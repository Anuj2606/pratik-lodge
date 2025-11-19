'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter, usePathname } from 'next/navigation';

import localFont from 'next/font/local';

const kugile = localFont({
  src: '../fonts/Kugile_Demo.ttf',
  variable: '--font-kugile',
  display: 'swap',
});

const aderoTrial = localFont({
  src: '../fonts/AderotrialRegular-ZVreq.otf',
  variable: '--font-adero-trial',
  display: 'swap',
});

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const router = useRouter();
  const pathname = usePathname();

  const goToSection = (id: string) => {
    if (pathname === '/') {
      const el = document.getElementById(id);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
        setIsMenuOpen(false); // close menu on mobile
      }
    } else {
      router.push(`/?scrollTo=${id}`);
    }
  };

  return (
    <div className="sticky top-0 z-50 bg-[#FFFFFF] text-[#3C3C3C] w-full mb-4 shadow-sm">
      <div className="relative flex items-center justify-between w-full mx-auto px-4 py-2 sm:px-6 md:px-10 lg:px-16 h-[72px]">

        <div className={`${kugile.className} text-2xl sm:text-4xl mt-2 md:mt-0 font-normal tracking-wider whitespace-nowrap`}>
          <Link href="/">Pratik Lodge</Link>
        </div>

        <div className={`${aderoTrial.className} hidden md:flex justify-center flex-1 gap-10 text-sm font-semibold`}>
          <button onClick={() => goToSection('about')} className="hover:text-yellow-500 hover:scale-105 transition-all delay-150 duration-100 ease-in-out cursor-pointer uppercase">
            About Us
          </button>
          <button onClick={() => goToSection('facilities')} className="hover:text-yellow-500 hover:scale-105 transition-all delay-150 duration-100 ease-in-out cursor-pointer uppercase">
            Facilities & Services
          </button>
          <button onClick={() => goToSection('gallery')} className="hover:text-yellow-500 hover:scale-105 transition-all delay-150 duration-100 ease-in-out cursor-pointer uppercase">
            Gallery
          </button>
          <button onClick={() => goToSection('location')} className="hover:text-yellow-500 hover:scale-105 transition-all delay-150 duration-100 ease-in-out cursor-pointer uppercase">
            Location
          </button>
          <Link href="/recommendations">
            <button className="hover:text-yellow-500 hover:scale-105 transition-all delay-150 duration-100 ease-in-out cursor-pointer uppercase flex items-center gap-1">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" className="w-4 h-4">
                <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
              </svg>
              Recommendations
            </button>
          </Link>
        </div>

        <div className="hidden md:flex items-center">
          <Link href="/contact">
            <button className={`${aderoTrial.className} bg-white text-[#3C3C3C] text-sm border border-[#3C3C3C] px-3 py-2 rounded-3xl hover:text-yellow-500 hover:scale-105 transition-all delay-150 duration-100 ease-in-out cursor-pointer`}>
              Reach Out
            </button>
          </Link>
        </div>

        {/* Hamburger for Mobile */}
        <div className="md:hidden flex items-center">
          <button onClick={() => setIsMenuOpen(!isMenuOpen)}>
            <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
              {isMenuOpen ? (
                <>
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </>
              ) : (
                <>
                  <line x1="4" y1="6" x2="20" y2="6" />
                  <line x1="4" y1="12" x2="20" y2="12" />
                  <line x1="4" y1="18" x2="20" y2="18" />
                </>
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden bg-white px-6 py-4 flex flex-col gap-4 text-sm font-semibold border-t">
          <button onClick={() => goToSection('about')} className="uppercase">About Us</button>
          <button onClick={() => goToSection('facilities')} className="uppercase">Facilities & Services</button>
          <button onClick={() => goToSection('gallery')} className="uppercase">Gallery</button>
          <button onClick={() => goToSection('location')} className="uppercase">Location</button>
          <Link href="/recommendations">
            <button className="uppercase flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" className="w-4 h-4">
                <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
              </svg>
              Recommendations
            </button>
          </Link>

          <Link href="/contact">
            <button className="px-6 py-2 text-center uppercase border border-[#3C3C3C] rounded-3xl mx-auto block">
              Reach Out
            </button>
          </Link>

        </div>
      )}
    </div>
  );
}
