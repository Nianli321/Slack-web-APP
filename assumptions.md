Login / Registering Assumption:
-	For an email to be valid it must contain @ and .com/au/org/net etc.. suffix.
-	The password is not allowed to be all whitespaces.
-	The password must be a combinations of numbers and characters.
-	When registering, the first-name and last-name can be any combination of lowercase and upper case characters. No numbers allowed. Cannot be whitespace.

Standup Assumptions:
-	Each time a user posts to the standup, we have to check if she/he is a member of the channel before posting.
-	A user can post to a standup on any channel, the channel doesn’t have to exist for the user to post a standup. This means that the user will be able to post to a channel standup from another channel. How else can he/she post to a standup on an incorrect channel.

Search Assumptions:
-	The search Function matches on keyword matching. So the string “Hello World” when searched is matched on “hello” and “word” separately.
-	There is a Arbitrary limit to searching. 1000 characters.

User assumptions:
-   A person's first or last name can't be updated to an empty string.
-   A person's handle can't be an empty string.
-   When uploading a photo, the URI given actually points to an image and not some other content type.

Admin assumptions:
-   An admin can demote another admin/owner to being member.
-   An admin can promote anyone to being an owner.
 
Channel assumptions:
-   A channel can have more than one owner
-   Only channel menbers can invite others to join the channel.
-   Only channel menbers can see the channel detials.
-   channels_list and channels_listall will return a list of dictionaries.
-   All the infomation of a channel is stored in a dictionary.
-   users can not join a private channel.
-   values returned by channel_details are stored in a dictionary, and represented as
    {'name': -----, 'owner_name': -----, 'all_members': ['----'','----'','----'']}.
-   values returned by channel_messages are stored in a dictionary, and represented as
    {'message':['---', '---','---'], 'start': inedx, 'end' : index}.

    
Messages assumptions:
-   In all current tests, it is assumed that a valid message_id is 1.
-   It is assumed that it is possible to get a message_id (no function currently gives one).
-   It is assumed that a valid react_id is 1.
-   It is assumed that you can't edit a message to have more then 1000 characters.
-   It is assumed that react_id's, channel_id's and message_id's cannot be negative.
-   It is assumed that you can't send a message from an invalid token.
