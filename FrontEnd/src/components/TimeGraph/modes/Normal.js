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

/**
 * Function provider for the normal view of a TimeGraph
 */
const NormalMode = {
  /**
   * Processes the API response into graph data
   * @param  {object} data json response from the api
   * @returns {object} labels and dataset
   */
  processGraphData(data) {
    const { labels } = data;
    const datasets = this.getDefaultDatasets();
    datasets[0].data = data.cves_count.length > 0 ? data.cves_count : [0];

    return { datasets, labels };
  },
  /**
   * Processes the API response into table data
   * @param  {object} data json response from the api
   * @returns {object} labels and table data
   */
  processTableData(data) {
    const { labels } = data;
    const table = data.cves;

    return { labels, table };
  },
  /**
   * Returns the options used for this mode
   * @returns {object} options for chartjs
   */
  getOptions(xLabel, yLabel, onClick, onHover) {
    return {
      responsive: true,
      maintainAspectRatio: false,
      legend: {
        display: false,
      },
      tooltips: {
        mode: 'index',
        intersect: false,
      },
      scales: {
        xAxes: [
          {
            stacked: true,
            scaleLabel: {
              display: true,
              labelString: xLabel,
            },
          },
        ],
        yAxes: [
          {
            stacked: true,
            ticks: {
              beginAtZero: true,
            },
            scaleLabel: {
              display: true,
              labelString: yLabel,
            },
          },
        ],
      },
      onClick,
      onHover,
    };
  },
  /**
   * Returns the default used dataset
   * @returns {array} default dataset
   */
  getDefaultDatasets() {
    return [
      {
        trendlineLinear: {
          style: '#45aaf2',
          width: 2,
        },
        label: 'vulnerabilities',
        data: [0],
        backgroundColor: '#fc5c65',
        borderColor: '#eb3b5a',
        borderWidth: 2,
      },
    ];
  },
};

/** @component */
export default NormalMode;
