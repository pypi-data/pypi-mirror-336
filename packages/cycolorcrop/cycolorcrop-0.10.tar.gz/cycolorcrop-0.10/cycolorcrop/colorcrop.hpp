#ifndef COLORCROP_HPP
#define COLORCROP_HPP
#include <cstdint>

void find_start_y(uint32_t* img, uint32_t* colors, int32_t width, int32_t height, int32_t color_length,
                  int32_t* start_y)
    {
    int32_t total_length{ width * height };
    bool match{};
    for (int32_t i{}; i < total_length; i++) {
        match = false;
        for (int32_t j{}; j < color_length; j++) {
            if (img[i] == colors[j]) {
                match = true;
                break;
                }
            }
        if (!match) {
            *start_y = i / width;
            return;
            }
        }
    }

void find_end_y(uint32_t* img, uint32_t* colors, int32_t width, int32_t height, int32_t color_length,
            int32_t* end_y)
    {
    int32_t total_length{ width * height - 1 };
    bool match{};
    for (int32_t i{ total_length }; i >= 0; i--) {
        match = false;
        for (int32_t j{}; j < color_length; j++) {
            if (img[i] == colors[j]) {
                match = true;
                break;
                }
            }
        if (!match) {
            *end_y = i / width;
            return;
            }
        }
    }
void find_start_x(uint32_t* img, uint32_t* colors, int32_t width, int32_t height, int32_t color_length,
                  int32_t* start_x)
    {
    bool match{};
    for (int32_t x{}; x < width; x++) {
        for (int32_t y{}; y < height; y++) {
            match = false;
            for (int32_t j{}; j < color_length; j++) {
                if (img[y * width + x] == colors[j]) {
                    match = true;
                    break;
                    }
                }
            if (!match) {
                *start_x = x;
                return;
                }
            }
        }
    }

void find_end_x(uint32_t* img, uint32_t* colors, int32_t width, int32_t height, int32_t color_length,
                int32_t* end_x)
    {
    bool match{};
    for (int32_t x{ width - 1 }; x >= 0; x--) {
        for (int32_t y{}; y < height; y++) {
            match = false;
            for (int32_t j{}; j < color_length; j++) {
                if (img[y * width + x] == colors[j]) {
                    match = true;
                    break;
                    }
                }
            if (!match) {
                *end_x = x + 1;
                return;
                }
            }
        }
    }

void find_coord(int32_t action, uint32_t* img, uint32_t* colors, int32_t width, int32_t height, int32_t color_length,
                int32_t* coord) {

    switch (action) {
            case 0:
                find_start_x(img, colors, width, height, color_length, coord);
                break;
            case 1:
                find_end_x(img, colors, width, height, color_length, coord);
                break;
            case 2:
                find_start_y(img, colors, width, height, color_length, coord);
                break;
            case 3:
                find_end_y(img, colors, width, height, color_length, coord);
                break;
            default:
                break;

        }
    }
#endif
