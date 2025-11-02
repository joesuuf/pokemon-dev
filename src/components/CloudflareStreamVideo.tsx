import React from 'react';
import { Stream } from '@cloudflare/stream-react';

interface CloudflareStreamVideoProps {
  videoId: string;
  className?: string;
}

export const CloudflareStreamVideo: React.FC<CloudflareStreamVideoProps> = ({
  videoId,
  className = ''
}) => {
  return (
    <div className={`cloudflare-stream-video ${className}`}>
      <Stream
        src={videoId}
        controls
        autoplay={false}
        preload="metadata"
        responsive
      />
    </div>
  );
};
