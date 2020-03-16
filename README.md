# Why DVAF?

The DVAF is a means to showcase progress in reproducible software security metrics resesarch. First of all, it offers the community with up-to-date information about vulnerability trends, types, etc. This high level view is crucial in assessing the general security landscape.
Second, it helps developers and maintainers assess the health of the projects they are working on and make the necessary adjustments in their development and patching processes.
Third, it is useful for developers and system administrators, helping them assess the attack surface of packages that they choose to use as dependencies, or install on their systems.
Finally, it also serves as a demonstrator for politicians, journalists, etc. to make them understand the problems the community faces.

In general, the front-end includes two types of plots. First, plots showing the number of vulnerabilities discovered over time.
These plots can be filtered by attributes (e.g. type, severity, release, year) and include trend lines.
Second, plots that show the ratio of different attributes over time (e.g. severity, types)

You can see it in action on https://mstar.tk.informatik.tu-darmstadt.de/
# Summary

- Overall Goal of the project: Develop a data gathering and visualization platform for vulnerabilities in Debian GNU/Linux packages.
- General requirements: extensibility, usability, (add third requirement here)
  - extensibility: Very important! (may be challenging - requires focus) New data, plots & metrics can be easily incorporated
  - usability: The graphical interface should be tested via a user study so as to be understandable
- Main components:
  - Back-end for data gathering: Should gather the required vulnerabiity data from DSAs, DLAs, and the NVD.
  - The main requirements here is that the data is complete and mistakes that are found can be manually corrected.
  - Front-end for visualization: Should include:
    - A general page with trends about the overall landscape (including number of vulnerabilities that you can filter by severity, release etc., types, plus trend lines)
    - A page per software package with similar information
    - A page where a user can upload a system configuration and get condensed information about her packages
    - A page with (graphical) documentation on how the system works
