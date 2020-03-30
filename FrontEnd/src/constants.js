/*
DVAF -  offers the security-research community with up-to-date information
        about vulnerability trends, types, etc.

Copyright (C) 2019-2020
Nikolaos Alexopoulos <alexopoulos@tk.tu-darmstadt.de>,
Lukas Hildebrand <lukas.hildebrand@stud.tu-darmstadt.de>,
Jörn Schöndube <joe.sch@protonmail.com>,
Tim Lange <tim.lange@stud.tu-darmstadt.de>,
Moritz Wirth <mw@flanga.io>,
Paul-David Zürcher <mail@pauldavidzuercher.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.
*/
import React from 'react';

export const BASE_URL =
  process.env.NODE_ENV === 'production' ? 'https://mstar.tk.informatik.tu-darmstadt.de' : 'http://predserver.tk.informatik.tu-darmstadt.de';

// Templates for InformationHelper
export const INFO_TEMPLATE = {
  debian: (
    <span>
      This data is collected from the <a href="https://tracker.debian.org/">Debian Package Tracker</a>.
    </span>
  ),
  nvd: (
    <span>
      This data is collected using <a href="https://www.cve-search.org">CVE Search</a>, which is crawling the data from the NVD database.
    </span>
  ),
  nvdwdeb: (
    <span>
      The package is from the Debian package repository. The CVEs are crawled from the{' '}
      <a href="https://security-tracker.debian.org/tracker/">Debian Security Tracker</a>. All further information about the CVEs such as
      publish date are from <a href="https://www.cve-search.org">CVE Search</a> and <a href="https://nvd.nist.gov">NVD</a> respectively.
    </span>
  ),
};
