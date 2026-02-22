import Footer from '@theme-original/Footer';
import React from 'react';

export default function FooterWrapper(props) {
  return (
    <div className="responsive-footer-container">
      <Footer {...props} />
    </div>
  );
}