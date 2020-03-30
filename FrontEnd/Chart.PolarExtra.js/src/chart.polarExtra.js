// no-automatic-copyright-generation
// This is written in non-ES6, so our eslint goes crazy
/* eslint-disable */
/*
 * PolarExtra
 *
 * dataset must contain
 *  data[]: length of slice
 *  width[]: width of slice
 *  color[]: color of slice
 *
 * options must contain
 *  widthBase: maximum value of width
 *  colorBase: maximum value of color
 *
 * optional options
 *  text: circle in the center with the text inside
 *  lengthLabel: label for length value
 *  widthLabel: label for width value
 *  colorLabel: label for color value
 *  alwaysShowLabel: whether the label is always visible or not
 *  toFixed: round to n decimal place
 */
(function (Chart) {
  var helpers = Chart.helpers;

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
  Chart.defaults.polarExtra.toFixed = 2;
  Chart.defaults.polarExtra.tooltips.callbacks.beforeLabel = function (tooltipItem, data) {
    var label =
      this._chart.options.lengthLabel +
      ': ' +
      Math.pow(2, data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]).toFixed(this._chart.options.toFixed) +
      '\n' +
      this._chart.options.widthLabel +
      ': ' +
      data.datasets[tooltipItem.datasetIndex].width[tooltipItem.index].toFixed(2).split(this._chart.options.toFixed)[0] +
      '\n' +
      this._chart.options.colorLabel +
      ': ' +
      data.datasets[tooltipItem.datasetIndex].color[tooltipItem.index].toFixed(2).split(this._chart.options.toFixed)[0];

    return label;
  };
  Chart.defaults.polarExtra.scale.ticks.callback = function (value, index, values) {
    return Math.round(Math.pow(2, value));
  }
  // Remove default tooltip content
  Chart.defaults.polarExtra.tooltips.callbacks.label = function () {
    return '';
  };

  var superClass = Chart.controllers.polarArea.prototype;

  Chart.defaults.polarExtra.opacity = 1;

  Chart.controllers.polarExtra = Chart.controllers.polarArea.extend({
    initialize: function initialize(chart, datasetIndex) {
      var color = function (number) {
        var percentage = number * 100;
        var r = percentage > 50 ? 255 : Math.floor((255 * percentage * 2) / 100);
        var g = percentage < 50 ? 255 : Math.floor(255 - (255 * (percentage * 2 - 100)) / 100);
        return "rgba(" + r + "," + g + ", 0, " + chart.config.options.opacity + ")";
      };

      // Overwrite color of slice
      chart.config.data.datasets[datasetIndex].backgroundColor = chart.config.data.datasets[datasetIndex].color.map(function (c) {
        return color(c / chart.config.options.colorBase);
      });
      chart.config.data.datasets[datasetIndex].data = chart.config.data.datasets[datasetIndex].length.map(function (e) { return Math.log(e) / Math.log(2); })

      superClass.initialize.call(this, chart, datasetIndex);
    },
    updateElement: function updateElement(arc, start, mode) {
      helpers.extend(arc, {
        draw: function draw() {
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
          var color2 = function (number, opacity) {
            var percentage = number * 100;
            var r = percentage > 50 ? 255 : Math.floor((255 * percentage * 2) / 100);
            var g = percentage < 50 ? 255 : Math.floor(255 - (255 * (percentage * 2 - 100)) / 100);
            return "rgba(" + r + "," + g + ", 0, " + opacity + ")";
          };
    
          this._chart.config.data.datasets[this._datasetIndex].backgroundColor = this._chart.config.data.datasets[this._datasetIndex].color.map(c => color2(c / this._chart.config.options.colorBase, this._chart.config.options.opacity));
          ctx.fillStyle = vm.backgroundColor;
          if (vm.borderColor === "#fff")
            ctx.strokeStyle = "transparent";
          else
            ctx.strokeStyle = "rgba" + vm.borderColor.substr(3, vm.borderColor.length - 4) + "," + this._chart.config.options.opacity + ")";

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
              this._chart.config.data.labels[this._index].substr(0, Math.floor(arc.outerRadius / this._chart.options.fontSize)),
              arc.x + (arc.outerRadius * Math.cos(arc.startAngle + (arc.endAngle - arc.startAngle) / 2)) / 2,
              arc.y + (arc.outerRadius / 2) * Math.sin(arc.startAngle + (arc.endAngle - arc.startAngle) / 2)
            );
          }

          if (vm.borderWidth) {
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