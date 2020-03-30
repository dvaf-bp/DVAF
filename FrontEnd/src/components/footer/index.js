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
import PropTypes from 'prop-types';

function Footer(props) {
  return (
    <footer className={props.className}>
      <hr />
      <div className="row">
        <div className="col-sm">
          © 2020 Copyright: DVAF{' '}
          <img src="https://travis-ci.com/mowirth/dvaf-frontend.svg?token=3pYLhWgBdLmhyWCVPfCP&branch=dev" alt="build status" />
        </div>
        <div id="SiteRef" className="col-sm">
          <div className="float-right">
            <a href="./dsgvo"> DSGVO </a> | <a href="./imprint">Imprint</a>
          </div>
        </div>
      </div>
    </footer>
  );
}

Footer.propTypes = {
  className: PropTypes.string,
};
Footer.defaultProps = {
  className: 'pt-3 ',
};

export default Footer;
