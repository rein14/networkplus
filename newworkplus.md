# NetworkPlus App API

## Base url: http://157.7.242.91:8010/api/
 
By using the following endpoint, URL is formed by baseurl + endpoint and API communication is performed.
  
## Main endpoints

| Endpoint name |  Link  | Method |  Purpose | DOC-CHECK |
|---|---|---|---|---|
|  Registration | /registration  |POST | Registartion for user | OK | 
|  Forget Password | /forget-password    | POST |  For Forget Password  | OK | 
|  Reset Password | /reset-password    | POST |  For Reset Password  | OK |
|  Login | /login    | POST |  For User Login  | OK |
|  Logout | /logout-user   | GET|  For User Logout | OK |
|  User | /user/< user_id >   | GET|  For User Details | OK |
|  User | /get-me   | GET|  For Getting Own Profile Information | OK |
|  Profile | /update-profile   | GET|  For Updating User Details | OK |
|  Follower | /follower   | GET|  For Adding New Follower | OK |
|  Follower | /get-follow-list   | GET|  For A Single User Follow List  | OK |
|  Search | /search   | GET|  For Searching User  | OK |
|  Notification | /get-notifications   | GET|  For User Notification | OK |
|  NearBy User | /get-nearby   | GET|  For Getting Nearby User | OK |


