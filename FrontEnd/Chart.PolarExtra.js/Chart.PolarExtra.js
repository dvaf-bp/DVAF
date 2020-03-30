/*!
 * Chart.PolarExtra.js
 * http://chartjs.org/
 * Version: 0.1.0
 *
 * Released under the MIT license
 */
(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
(function (Chart) {
  var helpers = Chart.helpers;
  var color = function (number) {
    var percentage = number * 100;
    var r = percentage > 50 ? 255 : Math.floor((255 * percentage * 2) / 100);
    var g = percentage < 50 ? 255 : Math.floor(255 - (255 * (percentage * 2 - 100)) / 100);
    return "rgb(" + r + "," + g + ", 0)";
  };

  Chart.defaults.polarExtra = helpers.merge({}, Chart.defaults.polarArea);
  Chart.defaults.polarExtra.backgroundColor = 'white';
  Chart.defaults.polarExtra.color = Chart.defaults.global.defaultFontColor;
  Chart.defaults.polarExtra.fontSize = Chart.defaults.global.defaultFontSize;

  Chart.defaults.polarExtra.text = '';
  Chart.defaults.polarExtra.lengthLabel = 'Length';
  Chart.defaults.polarExtra.widthLabel = 'Width';
  Chart.defaults.polarExtra.colorLabel = 'Color';
  Chart.defaults.polarExtra.widthBase = 1;
  Chart.defaults.polarExtra.colorBase = 1;
  Chart.defaults.polarExtra.alwaysShowLabel = false;

  // Disable padding for color
  Chart.defaults.polarExtra.tooltips.displayColors = false;
  // Label as title in tooltips
  Chart.defaults.polarExtra.tooltips.callbacks.title = function (tooltipItem, data) {
    return data.labels[tooltipItem[0].index];
  };
  // Values in tooltip
  Chart.defaults.polarExtra.tooltips.callbacks.beforeLabel = function (tooltipItem, data) {
    var label =
      this._chart.options.lengthLabel +
      ': ' +
      data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index] +
      '\n' +
      this._chart.options.widthLabel +
      ': ' +
      data.datasets[tooltipItem.datasetIndex].width[tooltipItem.index] +
      '\n' +
      this._chart.options.colorLabel +
      ': ' +
      data.datasets[tooltipItem.datasetIndex].color[tooltipItem.index];

    return label;
  };
  // Remove default tooltip content
  Chart.defaults.polarExtra.tooltips.callbacks.label = function () {
    return '';
  };

  var superClass = Chart.controllers.polarArea.prototype;

  Chart.controllers.polarExtra = Chart.controllers.polarArea.extend({
    initialize: function initialize(chart, datasetIndex) {
      // Overwrite color of slice


      superClass.initialize.call(this, chart, datasetIndex);
      chart.config.data.datasets[datasetIndex].backgroundColor = chart.config.data.datasets[datasetIndex].color.map(function (c) {
        return color(c / chart.config.options.colorBase);
      });
    },
    updateElement: function updateElement(arc, start, mode) {
      helpers.extend(arc, {
        draw: function draw() {
          console.log(this);
          var ctx = this._chart.ctx;
          var vm = this._view;

          // eslint-disable-next-line
          var arc = {
            x: vm.x,
            y: vm.y,
            innerRadius: vm.innerRadius,
            outerRadius: Math.max(vm.outerRadius, 0),
            pixelMargin: 0,
            startAngle: vm.startAngle,
            endAngle: vm.endAngle,
          };

          ctx.save();
          ctx.fillStyle = vm.backgroundColor;
          ctx.strokeStyle = vm.borderColor;

          var diff =
            ((arc.endAngle - arc.startAngle) *
              (1 - this._chart.config.data.datasets[this._datasetIndex].width[this._index] / this._chart.config.options.widthBase)) /
            2;
          ctx.beginPath();
          ctx.arc(arc.x, arc.y, arc.outerRadius, arc.startAngle + diff, arc.endAngle - diff);
          ctx.arc(arc.x, arc.y, arc.innerRadius, arc.endAngle, arc.startAngle, true);
          ctx.closePath();
          ctx.fill();

          if (this._chart.config.options.alwaysShowLabel && arc.outerRadius !== 0) {
            ctx.textAlign = 'center';
            ctx.font = Chart.defaults.global.defaultFontStyle + " " + this._chart.options.fontSize + "px " + Chart.defaults.global.defaultFontFamily;
            ctx.fillStyle = this._chart.options.color;
            ctx.fillText(
              this._chart.config.data.labels[this._index],
              arc.x + (arc.outerRadius * Math.cos(arc.startAngle + (arc.endAngle - arc.startAngle) / 2)) / 2,
              arc.y + (arc.outerRadius / 2) * Math.sin(arc.startAngle + (arc.endAngle - arc.startAngle) / 2)
            );
          }

          if (vm.borderWidth) {
            ctx.strokeStyle = vm.borderColor;
            ctx.lineWidth = vm.borderWidth;
            ctx.lineJoin = 'bevel';
            ctx.beginPath();
            ctx.arc(arc.x, arc.y, vm.outerRadius, arc.startAngle + diff, arc.endAngle - diff);
            ctx.arc(arc.x, arc.y, arc.innerRadius, arc.endAngle, arc.startAngle, true);
            ctx.closePath();
            ctx.stroke();
          }

          if (this._chart.options.text !== '') {
            ctx.fillStyle = this._chart.options.backgroundColor;
            ctx.beginPath();
            ctx.arc(arc.x, arc.y, ctx.measureText(this._chart.options.text).width, 0, 2 * Math.PI);
            ctx.closePath();
            ctx.fill();

            ctx.textAlign = 'center';
            ctx.font = Chart.defaults.global.defaultFontStyle + " " + this._chart.options.fontSize + "px " + Chart.defaults.global.defaultFontFamily;
            ctx.fillStyle = this._chart.options.color;
            ctx.strokeStyle = Chart.defaults.global.defaultColor;
            ctx.fillText(this._chart.options.text, arc.x, arc.y);
          }

          ctx.restore();
        },
      });

      superClass.updateElement.call(this, arc, start, mode);
    },
  });
}).call(this, Chart);
},{}]},{},[1]);
