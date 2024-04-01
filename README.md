# Backend for Sagor

# BRAINDUMP
I'm thinking on management commands that are run by crons.
- Publisher command
- Subscriber command

The subscriber will sub to all the topics and filter them w/ regex or smt.
The publisher will publish to all the topics (that'll be deduced from a simple loop over the gateways)

