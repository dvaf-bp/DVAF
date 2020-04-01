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
import Box from '../../components/Box';
// import InfiniteAutoplaySlider from '../../components/InfiniteAutoplaySlider';
// import { BASE_URL } from '../../constants';
// eslint-disable-next-line no-useless-concat
// const COLLAB_BASE_URL = 'http://localhost:3000' + '/img/collab';

function Doc() {
  return (
    <>
      <PageTitle>The Debian Vulnerability Analysis Framework</PageTitle>
      <p>
        <em>
          The DVAF is a framework to collect and visualize security-relevant data intended to showcase progress in reproducible research on
          software security metrics and measurement. It offers the community with up-to-date information about vulnerability discovery
          trends, types, and more advanced metrics (future feature). This high-level view is helpful in assessing the general security
          landscape. The DVAF can support developers and the public get insights about code quality, its evolution and factors affecting it.
        </em>
      </p>
      <div className="row">
        <div className="col-lg-4">
          <Box>
            <h2 style={{ textAlign: 'center' }}>Developers</h2>
            <p>
              DVAF helps developers and maintainers assess the health of their projects and make the necessary adjustments in their
              development and patching processes. It helps assessing the attack surface of packages that they use as dependencies for their
              projects or have installed on their systems.
            </p>
          </Box>
        </div>
        <div className="col-lg-4">
          <Box>
            <h2 style={{ textAlign: 'center' }}>People</h2>
            <p>
              The DVAF can serve as a demonstrator for politicians, journalists and other representatives to help them understand the
              problems faced by the community. But it doesn&rsquo;t stop there. It can be used as an educational tool for the public,
              hopefully producing a positive effect on the open source community, by providing incentives for improved security and patching
              processes.
            </p>
          </Box>
        </div>
        <div className="col-lg-4">
          <Box>
            <h2 style={{ textAlign: 'center' }}>The Process</h2>
            <p>
              The Debian Vulnerability Analysis Framework (DVAF) is a data gathering and visualization platform for vulnerabilities in
              Debian GNU/Linux packages. It will be open sourced in march and is designed to be easily extensible (to accommodate ongoing
              and future research on security metrics and measurement). You can actively contribute through feature-requests in this user
              study :)
            </p>
          </Box>
        </div>
      </div>
      <hr />
      <h2> Website-Structure</h2>
      <p>
        This Website is split into pages. These pages contain different views on the landscape of vulnerability analysis. <br /> There are
        five pages in total:
      </p>
      <div className="accordion" id="accordionExample">
        <div className="card">
          <div className="card-header" id="headingOne">
            <h2 className="mb-0">
              <button
                className="btn btn-link"
                type="button"
                data-toggle="collapse"
                data-target="#collapseOne"
                aria-expanded="false"
                aria-controls="collapseOne"
              >
                The General Page
              </button>
            </h2>
          </div>

          <div id="collapseOne" className="collapse" aria-labelledby="headingOne" data-parent="#accordionExample">
            <div className="card-body">
              The General Page displays general information on the number of packages involved in the current release (plus other general
              information) and plots of number of vulnerabilities over user-defined time-periods. The user can select to see a trend line,
              filter per attributes, etc. This view intends to provide an overview of vulnerability discovery rates over all packages and
              the required patching effort.
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-header" id="headingTwo">
            <h2 className="mb-0">
              <button
                className="btn btn-link collapsed"
                type="button"
                data-toggle="collapse"
                data-target="#collapseTwo"
                aria-expanded="false"
                aria-controls="collapseTwo"
              >
                The Search Page
              </button>
            </h2>
          </div>
          <div id="collapseTwo" className="collapse" aria-labelledby="headingTwo" data-parent="#accordionExample">
            <div className="card-body">
              In the Search Page, the user can search for specific Packages and get (a) general information about the package (e.g.
              composition of source code w.r.t. programming languages), and (b) information about the open and historical vulnerabilities
              affecting the package.
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-header" id="headingThree">
            <h2 className="mb-0">
              <button
                className="btn btn-link collapsed"
                type="button"
                data-toggle="collapse"
                data-target="#collapseThree"
                aria-expanded="false"
                aria-controls="collapseThree"
              >
                The Upload Page
              </button>
            </h2>
          </div>
          <div id="collapseThree" className="collapse" aria-labelledby="headingThree" data-parent="#accordionExample">
            <div className="card-body">
              Did you ever want to know how secure your System really is?
              <br />
              Yes? Then today is your lucky day! <br />
              Well... quantifying security is not an easy task, but this page aims to provide a view into several security metrics regarding
              packages in your system&lsquo;s configuration. This includes known open vulnerabilities (together with their severity and
              exploit vectors) as well as historical quality indicators for the development and patching processes of each package (future
              feature that will include vulnerability lifetimes and patching speed indicators).
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-header" id="headingThree">
            <h2 className="mb-0">
              <button
                className="btn btn-link collapsed"
                type="button"
                data-toggle="collapse"
                data-target="#collapseFive"
                aria-expanded="false"
                aria-controls="collapseFive"
              >
                The Information Page
              </button>
            </h2>
          </div>
          <div id="collapseFive" className="collapse" aria-labelledby="headingFive" data-parent="#accordionExample">
            <div className="card-body">
              The Documentation page contains all the information you need to get an insight in our project. It&rsquo;s the page you are
              currently on ;)
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-header" id="headingThree">
            <h2 className="mb-0">
              <button
                className="btn btn-link collapsed"
                type="button"
                data-toggle="collapse"
                data-target="#collapseFour"
                aria-expanded="false"
                aria-controls="collapseFour"
              >
                The Export Page
              </button>
            </h2>
          </div>
          <div id="collapseFour" className="collapse" aria-labelledby="headingFour" data-parent="#accordionExample">
            <div className="card-body">
              The Export-Page shows all necessary information to export our used data so you can use them in your Projects. This includes
              our Database containing the CVEs, CWEs, CPEs, DSAs, DLAs and Package Information as well as our source code. We want to make
              sure, that our project is fully transparent and completely adaptable to your situation and need. If you have questions about
              the code-components we also have a documentation for the Front-End and Back-End code!
            </div>
          </div>
        </div>
      </div>
      <hr />
      <h2>Behind The Scenes</h2>
      Behind the scenes, there is another service running, which collects all the necessary information, keeps it updated and supports the
      functionality of this website. <br />
      <br />
      It collects information from:
      <ul>
        <li> Mitre </li>
        <li> NVD </li>
        <li> Oval </li>
        <li> Metersploit </li>
        <li> Microsoft Bulletin </li>
        <li> Packet Storm</li>
        <li> Redhat </li>
        <li> US Army Cyber Command SSI </li>
        <li> Carson and Saint </li>
        <li> D2Sec </li>
        <li> Exploit Database </li>
        <li> Hacker News </li>
        <li> Vulnerability Lab </li>
      </ul>
      {/*
      <InfiniteAutoplaySlider
        bannerlinks={[
          '/100px-US_Army_Cyber_Command_SSI.png',
          '/CarsonSAINTlogoRibbon.png',
          '/d2sec.jpg',
          '/edb-banner-logo-white.png',
          '/HackerNews.png',
          '/Metersploit.png',
          '/MicrosoftLogo.png',
          '/Mitre.png',
          '/NVD-logo-carousel.png',
          '/oval_logo.jpg',
          '/ps_logo.png',
          '/Redhat.png',
          '/VULNERABILITY_LAB.jpg',
        ].map(linkPostFix => {
          return COLLAB_BASE_URL + linkPostFix;
        })}
      /> */}
      <br />
      <p> For technical details we will provide extensively documented code in our Github repository with additional details.</p>
    </>
  );
}

export default Doc;
