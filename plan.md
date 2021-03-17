# Slackr Design Plan

## Categories

The app requirements can be divided into several logical categories:
- Authentication
- Channels
- Messages
- Profiles
- Moderation (admins)
- Core UI (side bar, header, footer etc.)

## Priority

| Priority | Requirement         | Reasoning                                                                                                                                                              |
|----------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1        | Authentication      | Almost all other functions rely on having registered users                                                                                                             |
| 1        | Core UI             | Without the core UI (e.g. sidebar) there is no way to interact with other components of the app                                                                        |
| 2        | Channels            | Channels is one of the core functionalities of the app.                                                                                                                |
| 3        | Messages            | Messaging is the core functionality of the app, but has some dependencies on having channels implemented                                                               |
| 4        | Moderation (admins) | Not as critical to include immediately as other features don't rely heavily on this                                                                                    |
| 4        | Profiles            | While it is critical to store the initial user registration data i.e. during authentication, capabilities to edit the data can wait for other features to be developed |

## Time estimation

![Slackr Roadmap](https://i.imgur.com/NevqdU7.png)

## Software Tools for Iteration 2

The software tools that we are going to use to help us solve Iteration 2 are;

    1. GitLab Issue Board 
![Software Tool](https://i.imgur.com/6FgMwoS.png)

This issue board contains each User Story in its appropriate logical category in an easy to read format. Each group member will be assigned their work
from this issue board. This will allow each team member to complete their work collaboratively and efficiently. This software tool lets us 'tick off' what User Stories we 
have completed and what User Stories we have yet to complete.

    2. Slack
![Software Tool](https://i.imgur.com/D1z2q7j.png)

Slack is an online discussion platform that lets the group have conversations over the internet. This allows us to do the project together even when we are not in the same location.
This tool will allow us to resolve issues that team members have with their assigned work without being face-to-face

