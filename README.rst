DirtyRF
-----

Simulate the effect of dirty RF (IQ Imbalance, Phase Noise, Non-Linearities) on a complex symbol in python and MyHDL
This project was created in the context of my student project at the TU Dresden - Germany

*The development of wireless communications systems faces the technological limits set by analog RF front-ends. The conventional approach is to keep the analog RF design separated from the digital signal processing design. However, with today’s deep sub-micron technology, analog RF impairments are reaching a new problem level, requiring a paradigm shift in the design of transceivers. The key idea behind dirty RF is to analyze and model RF impairments such that the error effects caused by imperfect RF can be compensated by using proper digital baseband processing.*

*The use of software defined radio (SDR) platforms allows for an efficient and effective way to prototype new wireless communication systems. Compared to practical low cost lower power wireless transceivers, SDR is typically equipped with more advanced RF frontends. Therefore, the goal of this student work is to develop a dirty RF emulator, emulating practical RF impairments such as phase noise, non-linearities, I/Q imbalance, ADC impairments and so on. The integration of such a dirty RF emulator into the SDR platform (e.g., NI USRP-Rio) provides a near-practice platform for transceiver design, particularly investigating the impact of RF impairments and developing compensation algorithms in the digital baseband.*


Setup
-----

1. Installation
    run install.sh in the repositories root dir **as root**
  
2. Uninstall
    run uninstall.sh in the repositories root dir **as root**



Usage
-----

run an example of the module with just typing _dirtyrf_example_ in console

in python just type

    import dirtyrf


to use the module