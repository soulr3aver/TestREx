About:
------------------------------------------------------
TestREx is a testbed for repeatable exploits, which has as main features: 
* packing and running applications with their environments; 
* injecting exploits and monitoring their success; and
* generating security reports. 

We also provide a corpus of example applications, taken from related works or implemented by us.

Quick installation instructions:
------------------------------------------------------
1. Find the 'install.sh' script in the TestREx root folder and make it runnable:
    chmod +x install.sh

2. Run the 'install.sh' script and reboot your PC after it will stop
    sudo ./install.sh

3. Build the software specific containers by executing:
    sudo python [TestREx root folder]/util/build-images.py

References:
------------------------------------------------------
Stanislav Dashevskyi, Daniel Ricardo dos Santos, Fabio Massacci, Antonino Sabetta. "[TESTREX: a Testbed for Repeatable Exploits](https://www.usenix.org/conference/cset14/workshop-program/presentation/dashevskyi)" in 7th Workshop on Cyber Security Experimentation and Test (USENIX CSET'14)