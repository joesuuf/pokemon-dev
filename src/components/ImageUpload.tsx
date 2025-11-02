import React, { useCallback, useState } from 'react';

interface ImageUploadProps {
  onImageSelect: (file: File) => void;
  maxSize?: number;
  acceptedFormats?: string[];
}

export const ImageUpload: React.FC<ImageUploadProps> = ({
  onImageSelect,
  maxSize = 5 * 1024 * 1024, // 5MB
  acceptedFormats = ['image/jpeg', 'image/png', 'image/webp'],
}) => {
  const [preview, setPreview] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      const file = acceptedFiles[0];
      if (!file) return;

      // Validate size
      if (file.size > maxSize) {
        setError(`File too large. Maximum size: ${maxSize / 1024 / 1024}MB`);
        return;
      }

      // Create preview
      const reader = new FileReader();
      reader.onload = () => {
        setPreview(reader.result as string);
        setError(null);
        onImageSelect(file);
      };
      reader.readAsDataURL(file);
    },
    [maxSize, onImageSelect]
  );

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const files = [file];
      onDrop(files);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const files = Array.from(e.dataTransfer.files);
    onDrop(files);
  };

  return (
    <div className="w-full">
      <div
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
          transition-colors
          ${error ? 'border-red-500 bg-red-50' : 'border-gray-300 hover:border-blue-500'}
        `}
      >
        <input
          type="file"
          accept={acceptedFormats.join(',')}
          onChange={handleFileInput}
          className="hidden"
          id="image-upload"
        />
        <label htmlFor="image-upload" className="cursor-pointer">
          {preview ? (
            <div className="space-y-4">
              <img
                src={preview}
                alt="Preview"
                className="max-w-full max-h-64 mx-auto rounded"
              />
              <p className="text-sm text-gray-600">
                Click or drag to replace image
              </p>
            </div>
          ) : (
            <div className="space-y-2">
              <p className="text-lg font-medium">
                Drag & drop a card image, or click to select
              </p>
              <p className="text-sm text-gray-500">
                Supports: JPEG, PNG, WebP (max {maxSize / 1024 / 1024}MB)
              </p>
            </div>
          )}
        </label>
      </div>
      {error && (
        <p className="mt-2 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};
