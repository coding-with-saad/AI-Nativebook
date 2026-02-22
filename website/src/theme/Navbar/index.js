import Navbar from '@theme-original/Navbar';
import React from 'react';

export default function NavbarWrapper(props) {
  return (
    <div className="responsive-navbar-container">
      <Navbar {...props} />
    </div>
  );
}