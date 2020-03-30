import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ChartComponent from 'react-chartjs-2';
import 'Chart.PolarExtra.js';

class PolarExtra extends Component {
  constructor(props) {
    super(props);

    this.color = number => {
      const percentage = number * 100;
      const r = percentage > 50 ? 255 : Math.floor((255 * percentage * 2) / 100);
      const g = percentage < 50 ? 255 : Math.floor(255 - (255 * (percentage * 2 - 100)) / 100);
      return `rgb(${r}, ${g}, 0)`;
    };

    this.props.data.datasets[0].backgroundColor = this.props.data.datasets[0].color.map(c => this.color(c / this.props.options.colorBase));
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
