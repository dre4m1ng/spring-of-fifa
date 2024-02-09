import * as React from "react";

import { Card, CardContent } from "@/components/ui/card";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
} from "@/components/ui/carousel";

import Autoplay from "embla-carousel-autoplay";

export default function CarouselOrientation() {
  return (
    <Carousel
      opts={{
        align: "start",
        loop: true,
        watchDrag: false,
      }}
      orientation="vertical"
      className="w-full max-w-xs"
      plugins={[
        Autoplay({
          delay: 2000,
        }),
      ]}
    >
      <CarouselContent className="-mt-1 h-[200px] select-none">
        {Array.from({ length: 10 }).map((_, index) => (
          <CarouselItem key={index} className="pt-1 md:basis-1/1">
            <div>
              <Card>
                <CardContent className="flex items-center justify-center p-6">
                  <span className="text-3xl font-semibold">{index + 1}</span>
                </CardContent>
              </Card>
            </div>
          </CarouselItem>
        ))}
      </CarouselContent>
    </Carousel>
  );
}
