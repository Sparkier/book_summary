function rstrip(x: string) {
  // This implementation removes whitespace from the right side
  // of the input string.
  return x.replace(/\s+$/gm, "");
}

export function toSafeFilename(filename: string) {
  return rstrip(filename.substring(0, 250).replace(/[^a-z0-9 ]/gi, ""));
}
