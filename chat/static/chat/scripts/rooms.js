$(function() {
  
  let $chatWindow = $("#messages");
  let chatClient;
  let roomChannel;
  let username;

  // Print stuff to chat
  function print(infoMessage, asHtml) {
    let $msg = $('<div class="info">');
    if (asHtml) {
      $msg.html(infoMessage);
    } else {
      $msg.text(infoMessage);
    }
    $chatWindow.append($msg);
  }

// Print Stuff to Chat 
 function printMessage(fromUser, message) {
   let $user = $('<span class="username">').text(fromUser + ":");
   if (fromUser === username) {
     $user.addClass("me");
   }
   let $message = $('<span class="message">').text(message);
   let $container = $('<div class="message-container">');
   $container.append($user).append($message);
   $chatWindow.append($container);
   $chatWindow.scrollTop($chatWindow[0].scrollHeight);
 }

  // Get an access token for user
  
  $.getJSON(
    "/token",
    {
      device: "browser"
    },
    function(data) {
      // added user
      username = data.identity;
      print(
          '<span class="me">' +
          username +
          "</span>",
        true
      );

      
      Twilio.Chat.Client.create(data.token).then(client => {
        chatClient = client;
        chatClient.getSubscribedChannels().then(createOrJoinChannel);
      });
    }
  );

  function createOrJoinChannel() {
    let channelName = window.location.pathname.split("/").slice(-2, -1)[0];
  
    chatClient
      .getChannelByUniqueName(channelName)
      .then(function(channel) {
        roomChannel = channel;
        setupChannel(channelName);
      })
      .catch(function() {
        // No Channel -> Create it
        chatClient
          .createChannel({
            uniqueName: channelName,
            friendlyName: `${channelName} Chat Channel`
          })
          .then(function(channel) {
            roomChannel = channel;
            setupChannel(channelName);
          });
      });
  }  

  // Get Old Messages and setup
  function setupChannel(name) {
    roomChannel.join().then(function(channel) {
      print(
        `Joined channel ${name} as <span class="me"> ${username} </span>.`,
        true
      );
      channel.getMessages(30).then(processPage);
    });

    // New msges
    roomChannel.on("messageAdded", function(message) {
      printMessage(message.author, message.body);
    });
  }
  function processPage(page) {
    page.items.forEach(message => {
      printMessage(message.author, message.body);
    });
    if (page.hasNextPage) {
      page.nextPage().then(processPage);
    } else {
      console.log("Done loading messages");
    }
  }
  
  // sent new msg
  let $form = $("#message-form");
  let $input = $("#message-input");
  $form.on("submit", function(e) {
    e.preventDefault();
    if (roomChannel && $input.val().trim().length > 0) {
      roomChannel.sendMessage($input.val());
      $input.val("");
  }
});

});