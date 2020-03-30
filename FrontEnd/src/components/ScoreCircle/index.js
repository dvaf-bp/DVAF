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

const ScoreCircle = props => {
  const color = number => {
    const percentage = number * 10;
    const r = percentage > 50 ? 255 : Math.floor((255 * percentage * 2) / 100);
    const g = percentage < 50 ? 255 : Math.floor(255 - (255 * (percentage * 2 - 100)) / 100);
    return `rgb(${r}, ${g}, 0)`;
  };

  const svg = (w, h, t) => {
    const percent = props.number * 10;
    let deg = 180 * ((percent * 2) / 100) - 90;
    const r = 50;

    if (props.number > 50) deg += 180;

    const px = Math.cos((deg * Math.PI) / 180) * r + 50 + t / 2;
    const py = Math.sin((deg * Math.PI) / 180) * r + 50 + t / 2;

    let d = `M ${50 + t / 2} ${t / 2}`;
    if (percent > 50) d += ` A 50 50 0 0 1 ${50 + t / 2} ${100 + t / 2} A 50 50 0 0 1 ${px} ${py}`;
    else d += ` A 50 50 0 0 1 ${px} ${py}`;

    return (
      <svg
        style={{ display: 'block', margin: 'auto' }}
        xmlns="http://www.w3.org/2000/svg"
        version="1.1"
        viewBox={`0 0 ${100 + t} ${100 + t}`}
        width={w}
        height={h}
      >
        <g id="paths">
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
      {svg('64px', '64px', 8)}
      <Number>{props.number}</Number>
    </Circle>
  );
};

ScoreCircle.propTypes = {
  number: PropTypes.number.isRequired,
};

export default ScoreCircle;
