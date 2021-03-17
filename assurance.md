# Verification and Validation
We considered both the verification and validation of this product.

To consider we were building the correct product (validation) we wrote acceptance criteria (see below) and verified that this matches our given design specification. We also did some simple high level design modelling by seperating the program into simple components that interact (e.g. separating messages and users and authentication). We also did manual walkthroughs of the program  to verify we were meeting the user requirements.

To consider that the product was correctly functioning
(verification) we wrote unit tests to verify that our expected outputs matched our inputs. This was also constantly checked with Python coverage to ensure we were testing all parts of our program.
Static analysis was done using Pylint to help verify our code was correct and well structured as well.


# Acceptance criteria
### Profile

#### As a user, I like to be able to customise my default handle, so I can name myself how I want

-   The handle can be anything so long as It is 3 or more characters in length.
-   The handle can handle must be unique to the user.

#### As a user, I should be able to edit my first name and last name so I can control what information others see

-   The first name of the user should be restricted between 1 to 50 characters.
-   The last name of the user should be restricted between 1 to 50 characters.
-   There is no other limitation on what name a user can have.
-   The user can have numbers or special characters in his or her name.

#### As a user, I want to be able to change my email address, so I can manage my information and login
-   The email address given must be of a valid format: something@domain.com.
-   Each user should have a unique email address.
-   An email address cannot be used by the same person twice.

#### As a user, I should be able to see the profile of any other user (name and profile picture), so I can easily identify who I'm talking to
-   Each user should be able to display their firstname, lastname, profile picture and handle to other users.
-   This information should be readily available for other users to look at.

#### As a user, I should able upload a profile picture, so that I can be easily identified
- The profile picture uploaded can be of anything.

### Authentication

####  As a user, I want to be able to register to slackr, so that I can communicate with groups and teams that I am a member of
-  A person must be able to register to the slackr application using their email address, firstname, lastname and a password of their choosing.
-  A person must be logged in so that they can communicate with groups and teams.
-  A registered user can join groups.
-  The password the user registers with must be less than 6 characters long.

#### As a user, I want registering to require my first and last name so that other users can identify me
-   Users should be able to register an account with their first name amd last name
-   A user's first name has to be between 1 and 50 characters long (sensible).
-   A user's last name has to be between 1 and 50 characters long (sensible).
-   A user's name can only be from the English alphabet.

#### As a user, I want registering to require a email, so that slackr can update me via email
- The user must supply an email so that Slackr can send emails to it
- The email must follow the RFC specification for emails

#### As a user, I want registering to require a password, so that my account has some security
- Each account must be private
- Each account must be inaccessible to people who don't know the login password

#### As a user, I want the ability to reset my password if I have forgotten it, so that I do not get locked out of my account
- Each user can reset their password given the right email address
- A secret code sent to the users email is the key to reseting the users password for their Slackr account

#### As a user, I want to be able to log out, so that my account cannot be used while I'm away.
- Each user should be able to log out easily (in the interest of security)
- When a user has logged out their token must be invalidated (so others cannot replay old login sessions)

#### As a user, I want the login for slackr to require my email and password, so that no one else can use my account without my permission
- Each account must be unique to that user (i.e. each account requires a unique email)
- There can be only one registered email per account
- The email can be used to reset passwords
- When a user logs in, his or her session must be tracked with the use of a token so we do not need to send an email and password constantly for authentication

### Admin

#### As an slackr admin, I should have access to an admin panel to promote other users to admins, so I can control who has administrative powers
- Some users must be admins to some channels
- Admins should have the power to make others admins

### Channel

#### As a user, I want to be able to leave a channel, so that when I'm finished in a channel I don't keep getting notifications
- The user must be able to leave the channel with a click of a button.
- Each user can be notified about the channels activities on their respective device.

#### As an owner, I want to be able to promote other users to be an owner of my channel, so that others can use the owner features when needed
-   If a user is a channel owner they can promote other users from a click of a button.
-   The user promoted to a channel owner must be able to perform Owner only actions; like removing users from the channel and promoting users to owners.
-   If a user who is not an authorised user of the channel attempts to access information, An error is thrown.

#### As a user, I want to be able to join a channel an owner has invited me too, so that I can engage in the channel
- Each user should only be able to join a channel they have been invited to by that channel owner.
- The user should be given the choice of joining the channel or not.
- It should not be that the user is forced to join the channel.

#### As a channel owner, I want to be able to add other people to the channel, so that I can discuss with other people
- Owners must be given the power to add other people to the channel that they are an owner of.
- The user can be anyone given that they are a valid user of Slackr.

#### As a user, I want to see who the channel owner is, so I know who to contact for moderating purposes
- With the click of a button a user can see who the channel Owner is.
- The Channel owner must be given the privileges of removing users form their channel and promoting other users.

#### As a user, I want to be able to see all messages posted in the channel, so that the channel can discuss issues in a project
- A user should be able to see up to 50 messages.
- The user should be notified that there are no more messages after they have seen 50 messages.
- Only authorised users should be able to see the messages of the channel.
- We tested this by giving different inputs to channel_messages function. Our tests basically include all the cases that may happen.
- The output would be including the start index and the end index, and a list of dictionaries. For each dictionary, it contains all the information of one piece of meaasge.
- All the messages can be shown by channel_messages function, so channel members can see the messages, hence they can interact with each other.

#### As a user, when viewing a channel, I want the channel name to always be visible, so I know which channel I'm talking in
-   The channel should should always be visible to users who are members of the channel.
-   The channel should be clearly outlined to describe what channel it is, and who the owners are so that the user knows what channel they are in.
-   We implemented chanenl data structure as a list of channel dictionaries, for each dictionary we would have a key holding the name of that channel.
-   And we also have a key which holds the channel_id which is a unique value. It can identify the channels. So it would be clear for users about which channel they are talking in.


#### As a user, I want to have the option to open my own channel, so that I can begin discussions on new topics
- Each user has the power to create their own channel.
- Once the user creates their channel they become an owner of their channel.
- Once an Owner the user can start to invite people to the channel.
- The channel name must not be longer than 20 characters in length.

#### As a user, I want to have a list of all channels I have access too, so that I can easily manoeuvre between the channels
- Users should be able to click on an item in a list of channels to join a particular channel.
- One channel must not be regarded more important than any other channel.
- Channels' ID must be unique, so we can identify each channel in the list

#### As a user, I want to know who else is currently in a channel and their roles in the channel, so that I know who I'm talking to in the channel
- Members of a channel must be able to clearly see who else is a member of the channel.
- All the mambers' infomation including their u_ids, names would be stored in channel.


### Search

#### As a user, I should be able to search for messages, so I can quickly reference something that has been said
- Users must be given the power to search all channels the user has joined for messages.

### Messages

#### As a user, I would like to be able to summarise the next 15 minutes using a "standup" command, so I can effectively use slackr for standups
- A member of a channel should be able to summarise the next 15 minutes of conversation into a standup.
- No none-members of the channel can initiate a standup.
- 15 minutes of conversation are accumulated into a list that no one can see until the 15 minutes is up.

#### As a user, I'd like to be able to send delayed messages, so I can send messages at the most appropriate time
- A user should be able to choose the time that he/she sends messages to the channels that they are members of.
- The user cannot send a message larger than 1000 characters.
- An error is displayed if the user tries to send a message to a channel that they are not a part of.

#### As a user, I'd like to be able to delete messages, so that I can remove irrelevant or mistaken messages
- If I make a mistake typing a message, I want to be able to delete that message ASAP.

#### As a user, I'd like to be able to react/unreact to messages, so I can quickly acknowledge a message without cluttering the message history
- Users can react to messages, with a thumbs up.
- The message must exist for the user to react to.
- The user must be part of the same channel they want to react to.

#### As a user I should be able to pin/unpin messages, so that I can easily keep important information visible
- A user of a channel should be able to pin or unpin important messages.
- pinned messages can be viewed later at any time.
- THe pinned messages are clearly visible to the user who pinned them.

#### As a user I should be able to edit messages, so I can fix small mistakes made when typing
- A user should be able to fix any mistakes in their messages even after they have typed them.

#### As a user, I should be able to send messages so I can communicate with other users
- As long as the user is a member of a channel, they should have the power to send messages to other users.


