from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import ProfileSerializer


import os
import requests
import cognitive_face as CF
import cv2
import time

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') 
    else: 
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        
    return render(request, 'users/profile.html',{'u_form': u_form,'p_form': p_form, 'verified' : request.user.profile.verified})


@login_required
def webcam(request):
        return render(request, 'users/verify.html')



def take_photo(request):

    ret = None
    video_capture = cv2.VideoCapture(0)
    # Check success
    if video_capture is None or not video_capture.isOpened():
        ret = False
    else:  
        for i in range(30):
            temp = video_capture.read()  

    # Read picture. ret === True on success
        ret, frame = video_capture.read()
        cv2.imwrite(os.path.join('testpic2.jpg'),frame)
    # Close device
    video_capture.release()
    
    # Need to save image as an url
    # Need to save numpy array and get URL 
    photo_path = os.path.join('testpic2.jpg')
    return {'photo_taken' : ret, 'photo_path' : photo_path} 


def set_verified(request, val):
    p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    if p_form.is_valid():
        obj = p_form.save(commit=True)
        obj.verified = val
        obj.save()


@login_required
def face_verification(request):
    
    print("ran face_verification")

    webcam_pic = take_photo(request)

    print("photo completed")

     # should render if photo taken sucessfully/unsuccesful pop up (Templats)
    if webcam_pic['photo_taken'] == False:
        messages.error(request, 'Could not detect webcam please try again')
        return webcam(request)
        print("Photo Not Taken")
    else:
        # Need a Pop Up
        #messages.success(request, 'Sucessfully taken photo, verfication in process....')
            
        # Get Profile Image
        if request.user.is_authenticated: 
            #image_serializer = ProfileSerializer(request.user.profile,context={"request": request})
            #profile_img_url = image_serializer.data
            profile_img_url = '/home/nyle/Desktop/django/bettingsite/Betting_Site' + request.user.profile.image.url
            webcam_img_path =  os.path.join('testpic2.jpg')

            # Need to check if the path are correct

            KEY = os.environ.get('Face_Verification')
            CF.Key.set(KEY)
           
            BASE_URL = 'https://canadacentral.api.cognitive.microsoft.com/face/v1.0'
            CF.BaseUrl.set(BASE_URL)
            # Call API and get Face_id's img 1 / img 2 
            img1json = CF.face.detect(profile_img_url)
            img2json = CF.face.detect(webcam_img_path)

            # Need a check to see if a profile picture is even a face picture
            if len(img1json) == 0:
                messages.error(request, 'Please change your profile picture to a picture of your face, then retry')
                set_verified(request, False)
            else:
            # If photo taken is not a face picture retake
                if len(img2json) == 0:
                    messages.error(request, 'The webcam did not get a picture of your face. Please verifiy again and make sure to look in the webcam!')
                    set_verified(request, False) 
                else: 
                    # Verifiy
                    faceID1 = img1json[0]["faceId"]
                    faceID2 = img2json[0]["faceId"]

                    verifyjson = CF.face.verify(faceID1,faceID2)
                    # Just means the confidence is greater than 0.5 (not the best)
                    #microsoft_verified = verifyjson["isIdentical"] 
                    #  Confidence is greater than 0.7
                    verified = (verifyjson["confidence"] >= 0.7)
                    
                    # Adding to the database field
                    set_verified(request, verified)
                    # Need to Add that To the Person Tag or Somthing
                    # So it shows up on profile

                    if verified:
                        messages.success(request, 'Your profile has been verified!')
                    else:
                        messages.error(request, 'Your face was not a match, please try again! Your profile has not been verfied!')
        else:
            return redirect('login') 
    return profile(request)



    

        
