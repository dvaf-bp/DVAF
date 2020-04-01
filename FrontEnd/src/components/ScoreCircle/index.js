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
import styled from 'styled-components';
import React from 'react';
import PropTypes from 'prop-types';

/**
 * Number with a circle outline to visualize a score
 */
const ScoreCircle = props => {
  const color = number => {
    const percentage = number * 10;
    const r = percentage > 50 ? 255 : Math.floor((255 * percentage * 2) / 100);
    const g = percentage < 50 ? 255 : Math.floor(255 - (255 * (percentage * 2 - 100)) / 100);
    return `rgb(${r}, ${g}, 0)`;
  };

  /*
    w: width in px
    h: height in px
    t: circle thickness in px
    o: outline thickness in px
    ocolor: outline color
  */
  const svg = (w, h, t, o, ocolor) => {
    const percent = props.number * 10;
    let deg = 180 * ((percent * 2) / 100) - 90;
    const r = 50;

    if (props.number > 50) deg += 180;

    const px = Math.cos((deg * Math.PI) / 180) * r + 50 + t / 2 + o;
    const py = Math.sin((deg * Math.PI) / 180) * r + 50 + t / 2 + o;

    let d = `M ${50 + t / 2 + o} ${t / 2 + o}`;
    if (percent > 50) d += ` A 50 50 0 0 1 ${50 + t / 2 + o} ${100 + t / 2 + o} A 50 50 0 0 1 ${px} ${py}`;
    else d += ` A 50 50 0 0 1 ${px} ${py}`;

    return (
      <svg
        style={{ display: 'block', margin: 'auto' }}
        xmlns="http://www.w3.org/2000/svg"
        version="1.1"
        viewBox={`0 0 ${100 + t + 2 * o} ${100 + t + 2 * o}`}
        width={`${w}px`}
        height={`${h}px`}
      >
        <g id="paths">
          <circle cx={50 + t / 2 + o} cy={50 + t / 2 + o} r={r + t / 2 + o / 2} stroke={ocolor} fill="transparent" strokeWidth={o} />
          <circle cx={50 + t / 2 + o} cy={50 + t / 2 + o} r={r - t / 2 - o / 2} stroke={ocolor} fill="transparent" strokeWidth={o} />
          <path d={d} style={{ fill: 'transparent', stroke: color(props.number), strokeWidth: t }} />
        </g>
      </svg>
    );
  };

  const Circle = styled.div`
    position: relative;
    text-align: center;
  `;

  const Number = styled.div`
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 1.5rem;
  `;

  return (
    <Circle>
      {svg(props.size, props.size, props.thickness, props.outlineThickness, props.outlineColor)}
      <Number>{props.number}</Number>
    </Circle>
  );
};

ScoreCircle.propTypes = {
  /** Score */
  number: PropTypes.number.isRequired,
  /* Size in px */
  size: PropTypes.number,
  /* Thickness of the colored */
  thickness: PropTypes.number,
  /* Thickness of the outline */
  outlineThickness: PropTypes.number,
  /* Color of the outline */
  outlineColor: PropTypes.string,
};

ScoreCircle.defaultProps = {
  size: 64,
  thickness: 14,
  outlineThickness: 2,
  outlineColor: '#BBBBBB',
};

export default ScoreCircle;
