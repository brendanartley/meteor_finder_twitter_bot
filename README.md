# meteor_finder_twitter_bot

- This Meteor Finder Twitter Bot is a tool that allows users to quickly and accurately locate the nearest known location where a meteor has made contact with the earths surface. The two key parts of the project are utilizing the Twitter API to reply to tweets, and calculating the nearest meteor landing site based on the location provided by the user. 

- To utilize this program a twitter user simply has to tweet their location ie "Wilmington, Delaware" with the hashtag #meteorfinder, and they would get a reply within 15 seconds of the closest meteor landing site to them, and some information about that meteor.


HOW THIS WAS DONE:

- By using NASA's Meteorite Landings dataset, I was able to retrieve coordinates from every meteorite landing site recorded. I was able to find the closest realtive location by using haversines formula (distance between two points on a sphere). I was then able to loop through the entire dataset and retrieve the closest point to any location on earth in <5secs, which is reasonable for this use case. Once the closest meteor landing location was known I retrieved some more information from that specific row and included that in the text body I was preparing for a reply tweet. 

- With the closest meteor location and reply info sorted, I used google maps to provide a link to the twitter user with a location marker which provided directions to the closest metoer landing location.

- I thought was a pretty cool application of Twitter's API, as it provides a quick and easy way for astronomical enthusiaststs to go looking for these cool sites.


NOTE: if you want to use this program yourself, make sure to visit developer.twitter.com to create access_keys and consumer_keys so that the program is linked to your account!




