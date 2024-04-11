# ArchivesSpace Digital Objects Tag Strip
## Description
This is a quick and dirty script for stripping excess HTML tags from digital objects for a smoother preservica import workflow.
## Prerequisites
This code was written for Python 3.12, with ArchivesSpace v3.4.1 in mind. Other versions of ArchivesSpace and Python may work, but are presently untested.
In order to use this code, you must have a username and password to the ArchivesSpace server which is configured for write level API access on the repository you intend to modify.
## Setup
Download the files. Run `pip install requirements.txt` in your shell of choice within the working directory. Configure the program as described below, and then run `digital_object_tag_strip.py` using Python.
## Configuration
At present, the configuration system for this project is not yet fully implemented. This can, as such, be expected to change in the future.
### ArchivesSpaceConnection.txt
This program expects a file named "ArchivesSpaceConnection.txt" to exist in the same folder as it
This file MUST be formatted as follows

```
ArchivesSpace API Endpoint (usually https://<FQDN FOR STAFF UI>/api/)
API User Username
API User Password
```

### Preservica URL
At present the preservica URL is not cleanly configured anywhere. As such, please modify line 76 of `digital_object_tag_strip.py` to reflect your Preservica URL. In the future, this will not be hardcoded.
## Use
Simply run the program, and an interactive prompt will talk you through the process. When it asks for a repository number, use the number that appears at the end of URL for the repository overview page. For example
https://archives.lib.rochester.edu/repositories/2 would have the repository number 2.
## TODO List
- [ ] Refactor code to completely meet PEP 8 standards.
- [ ] Add exception handling
- [ ] Improve logging
- [ ] Remove U of R url and make it configurable
- [ ] Rewrite the format of the config file
- [ ] Handle API keys more securely using the system keychain
- [ ] Add an optional UI
- [ ] Write better comments
- [ ] Add tests
- [ ] Add a connection test system
- [ ] Integrate functionality into ArchivesSpace Collections Manager project when that project is ready.
- [ ] List available repositories by number
## Credits
Code was written by [Channing Norton](https://www.github.com/C-Norton), on behalf of the University of Rochester River Campus Libraries. Special thanks to John Dewees for the request/ idea, and assistance on implementation and publication. All code contributed must first be run through the [Black](https://pypi.org/project/black/) code formatter, and comply to PEP 8 standards in full.
## Contributing
External contributions to this project are accepted, but it should be noted that this is a fairly low priority project for which the MVP has already been delivered. As such, while PRs and issues will be examined, it may take some time for them to be responded to.
## Notes on ArchivesSpace Database
This code modifies the ArchivesSpace database using the REST API. As such, a consistent internet connection must be ensured prior to running the script. Always back up your database before running the script. Neither myself, other contributors, nor the University of Rochester are responsible for damage to your database caused by this script. As always, be cautious, and proceed at your own risk.
## License
This code is licensed under the GNU GPLv3 license. See the license file in this repository for the full text and terms.
