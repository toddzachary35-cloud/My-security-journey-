# Tails OS Bootable USB

A writeup of my Tails OS setup, built to understand privacy-focused, amnesic operating systems and how anonymity tooling actually works under the hood.

## What is Tails?

Tails (The Amnesic Incognito Live System) is a live operating system you boot from a USB stick. By default it leaves no trace on the host machine and routes all network traffic through **Tor**, making it a standard tool in the privacy and digital security space.

## What I Set Up

- **Bootable USB install** of Tails, running independently of the host machine's own OS
- **Persistent storage** — an encrypted partition on the USB so that settings, files, and configuration survive between reboots, since Tails is amnesic by default and normally forgets everything on shutdown
- **Tor bridge connection** — configured a bridge rather than connecting to the public Tor network directly, useful in situations where Tor is blocked or monitored at the network level

## Why I Built This

This wasn't about needing anonymity day-to-day, it was about understanding how anonymity infrastructure actually works: how Tor routing differs from a VPN, why persistence has to be deliberately configured on an amnesic system, and what bridges solve that a normal Tor connection doesn't. That understanding matters for offensive security too, since obfuscating traffic and understanding what defenders can and can't see is relevant on both sides of the fence.

## Related Concepts Explored

- **VPN-over-Tor vs. Tor-only** — the tradeoffs between the two and when each makes sense
- **Transparent proxying** — routing all traffic through Tor at the network level rather than per-application

## Notes

This project was purely educational, exploring how privacy tooling works rather than any operational use case.
