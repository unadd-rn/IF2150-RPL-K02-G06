export const IMAGES = {
  logo: '/save_bite.png',
} as const;

export type ImageKey = keyof typeof IMAGES;