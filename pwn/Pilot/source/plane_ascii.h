#ifndef PLANE_ASCII_H
#define PLANE_ASCII_H

/**
 * @file plane_ascii.h
 * @brief Header file for plane ASCII animations
 * 
 * This library provides functions to display ASCII art animations 
 * of a plane flying freely or crashing.
 */

/**
 * @brief Show animation of plane flying freely with clouds
 * 
 * @param duration_seconds How long to show the animation (default: 10 if <= 0)
 * @return 0 on success, 1 if user quit, negative value on error
 */
int show_plane_flying(int duration_seconds);

/**
 * @brief Show animation of plane crashing into the ground
 * 
 * @return 0 on success, 1 if user quit, negative value on error
 */
int show_plane_crash(int duration_seconds);

#endif /* PLANE_ASCII_H */