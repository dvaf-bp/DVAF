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
import PageTitle from '../../components/pagetitle';
import QuestionHelper from '../../components/questionHelper';

function ExportData() {
  return (
    <>
      <div id="main" className="col-12 col-md-11 col-xl-10">
        <PageTitle>Export the Data</PageTitle>
        <h2 style={{ marginTop: '3rem' }}> Where can I get all the data you are using?</h2>
        <p>
          All the data we are using is directly <a href="/download">downloadable</a> or accessible as described in our{' '}
          <a href="/info">Information</a>.
        </p>
        <div>
          <h2 style={{ marginTop: '3rem' }}>Where does the data come from?</h2>
          <p>Everything is managed in a MongoDB database. We have several resources where we get our data from:</p>
          <ul>
            <li>
              <div>
                <h3 style={{ marginTop: '3rem' }}>CVE-Search</h3>
                <p>From CVE-Search we currently use the following data sets:</p>
                <ul>
                  <li>
                    <QuestionHelper elaboration="shortcut_cve">cves</QuestionHelper> - source NVD NIST (JSON)
                  </li>
                  <li>
                    <QuestionHelper elaboration="shortcut_cpe">cpe</QuestionHelper> - source NVD NIST
                  </li>
                  <li>
                    <QuestionHelper elaboration="shortcut_cwe">cwe</QuestionHelper> - source NVD NIST
                  </li>
                  <li>
                    <QuestionHelper elaboration="shortcut_capec">capec</QuestionHelper> - source NVD NIST
                  </li>
                </ul>
                <p>
                  See <a href="https://github.com/cve-search/cve-search">CVE-Search</a> for more information.
                </p>
              </div>
            </li>
            <li>
              <div>
                <h3 style={{ marginTop: '3rem' }}>Debian</h3>
                <p>
                  From Debian&apos;s Ultimate Debian Database (<a href="https://wiki.debian.org/UltimateDebianDatabase/">UDD</a>) we get all
                  the package information. To connect the packages to the vulnerabilities we parse the Debian Security Tracker JSON (
                  <a href="https://security-tracker.debian.org/tracker/">JSON</a>).
                </p>
              </div>
            </li>
          </ul>
        </div>
        <div>
          <h2 style={{ marginTop: '3rem' }}> How is the data structured?</h2>
          <p> We supply a MongoDB with the folling important collections:</p>
          <ul>
            <li>
              cves (Common Vulnerabilities and Exposure items) - All the official vulnerabilities, released by NIST. Items in this
              collection have all info related to each CVE
            </li>
            <li>
              cpe (Common Platform Enumeration items) - All the official products, released by NIST. Some of these have a human readable
              title.
            </li>
            <li>cwe (Common Weakness Enumeration items) - Information about Common Weaknesses, as published by NIST</li>
            <li> d2sec - Information about CVE&apos;s, as released by d2sec</li>
            <li>capec - (Common Attack Pattern Enumeration and Classification) - source NVD NIST</li>
          </ul>
          <p>There exist other collections used for internal caching</p>
        </div>
      </div>
    </>
  );
}

export default ExportData;
