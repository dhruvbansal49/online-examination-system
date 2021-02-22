(function () {
    'use strict';

    // ----------------------------------------------------
    // Configure Pusher instance
    // ----------------------------------------------------

    var pusher = new Pusher('a60f02f7bde182f427ce', {
        authEndpoint: '/pusher/auth',
        cluster: 'ap2',
        encrypted: true
      });

    // ----------------------------------------------------
    // Chat Details
    // ----------------------------------------------------

    let chat = {
        messages: [],
        currentRoom: '',
        currentChannel: '',
        subscribedChannels: [],
        subscribedUsers: []
    }

    // ----------------------------------------------------
    // Subscribe to the generalChannel
    // ----------------------------------------------------

    var generalChannel = pusher.subscribe('general-channel');

    // ----------------------------------------------------
    // Targeted Elements
    // ----------------------------------------------------

    const chatBody = $(document)
    const chatRoomsList = $('#rooms')
    const chatReplyMessage = $('#replyMessage')

    // ----------------------------------------------------
    // Register helpers
    // ----------------------------------------------------

    const helpers = {

        // ------------------------------------------------------------------
        // Clear the chat messages UI
        // ------------------------------------------------------------------

        clearChatMessages: () => $('#chat-msgs').html(''),

        // ------------------------------------------------------------------
        // Add a new chat message to the chat window.
        // ------------------------------------------------------------------

        displayChatMessage: (message) => {
            console.log(names,message.email)
            var n=names.includes(message.email)
            if(n==true)
            {
            if (message.email === chat.currentRoom) {


                $('#chat-msgs').prepend(
                    `<tr>
                        <td>
                            <div class="sender" style="text-align:right;font-size:12px;"><strong>~ ${message.sender} @ <span class="date">${message.createdAt}</span></strong></div>
                            <div class="message">${message.text}</div>
                        </td>
                    </tr>`
                )
            }
        }
        else{
            console.log("not found");
        }


        },

        // ------------------------------------------------------------------
        // Select a new guest chatroom
        // ------------------------------------------------------------------

        loadChatRoom: evt => {
            chat.currentRoom = evt.target.dataset.roomId
            chat.currentChannel = evt.target.dataset.channelId

            if (chat.currentRoom !== undefined) {
                $('.response').show()
                $('#room-title').text("Connected to "+evt.target.dataset.roomId)
            }

            evt.preventDefault()
            helpers.clearChatMessages()
        },

        // ------------------------------------------------------------------
        // Reply a message
        // ------------------------------------------------------------------
        replyMessage: evt => {
            evt.preventDefault()

            let createdAt = new Date()
            createdAt = createdAt.toLocaleString()

            const message = $('#replyMessage input').val().trim()

            chat.subscribedChannels[chat.currentChannel].trigger('client-support-new-message', {
                'name': 'Admin',
                'email': chat.currentRoom,
                'text': message, 
                'createdAt': createdAt 
            });

            helpers.displayChatMessage({
                
                'email': chat.currentRoom,
                'sender': 'tea_name',
                'text': message, 
                'createdAt': createdAt
            })


            $('#replyMessage input').val('')
        },
    }


      // ------------------------------------------------------------------
      // Listen to the event that returns the details of a new guest user
      // ------------------------------------------------------------------

      generalChannel.bind('new-guest-details', function(data) {

        chat.subscribedChannels.push(pusher.subscribe('private-' + data.email));

        chat.subscribedUsers.push(data);

        // render the new list of subscribed users and clear the former
        $('#rooms').html("");
        chat.subscribedUsers.forEach(function (user, index) {
            var n1=names.includes(user.email)
            if(n1==true)
            {
        
                $('#rooms').append(
                    `<li class="nav-item"><a style="background-color: #f44336; color: white;padding:7px 7px; text-align: center;text-decoration: none; margin-bottom:4px;display:inline-block"  data-room-id="${user.email}" data-channel-id="${index}" class="nav-link" href="#">${user.name}</a></li>`
                )
            }
            else{
                console.log("Nothing")
            }
        })
    
      })


      // ------------------------------------------------------------------
      // Listen for a new message event from a guest
      // ------------------------------------------------------------------

      pusher.bind('client-guest-new-message', function(data){
          helpers.displayChatMessage(data)
      })


    // ----------------------------------------------------
    // Register page event listeners
    // ----------------------------------------------------

    chatReplyMessage.on('submit', helpers.replyMessage)
    chatRoomsList.on('click', 'li', helpers.loadChatRoom)
}())