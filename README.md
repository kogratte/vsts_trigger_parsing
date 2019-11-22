# vsts_trigger_parsing
This small little tool is here to help you to configure your CI triggers, and your branch policies.

In the following situation:

Project A => Reference Project B

If project B is modified, then project A also need to be built to ensure quality. We can imagine that A unit tests may fail.

This tool examine your sln files, and extract external references. From that, it generate all the triggers you need to configure in your build definition, and also the one line path filter for branch policy.

Usage:

./analyse_triggers.py <Path to your repository> > result.txt
