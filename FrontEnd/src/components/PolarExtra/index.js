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
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ChartComponent from 'react-chartjs-2';
import 'Chart.PolarExtra.js';

class PolarExtra extends Component {
  constructor(props) {
    super(props);
    this.props.data.datasets[0].backgroundColor = [];
  }

  render() {
    // This is how react-chartjs-2 is doing chart bindings, which does violate our eslint rules, but I think it's ok to disable it here.
    // eslint-disable-next-line
    return <ChartComponent {...this.props} ref={ref => (this.chartInstance = ref && ref.chartInstance)} type="polarExtra" />;
  }
}

PolarExtra.propTypes = {
  data: PropTypes.oneOfType([PropTypes.object, PropTypes.func]).isRequired,
  options: PropTypes.oneOfType([PropTypes.object]),
};

PolarExtra.defaultProps = {
  options: {},
};

export default PolarExtra;
