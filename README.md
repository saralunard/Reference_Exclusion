# Reference_Exclusion

Problem: remixes, remasters, or tracks containing sampled tracks contain a reference exclusion to avoid mismatches against the original. This makes the track not safe for licensing due to the likelyhood of the track causing mismatches especially if the sampled clip is uses in isolation. 

Solution: This script calls the YouTube API to check for reference exclusions and exports a CSV which can be easily read by non eng. team members. The tracks can then be deactivated to ensure compliance. 
