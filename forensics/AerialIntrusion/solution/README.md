# writer writeup 
After analysis and discovering the segmented patters that are even.

tshark -r capture.pcap --export-objects "http,extracted_ts"

Remove odd segments
for i in $(seq 1 2 321); do rm -f segment${i}.ts; done

Merge even segments
cat $(seq -f "segment%g.ts" 2 2 322) > merged.ts

Adjust format
cp merged.ts ../enc.mp4

Read the keys from license and decode JWT

And after that decrypt

mp4decrypt \
  --key 1:0123456789abcdef0123456789abcdef \
  --key 2:abcdef0123456789abcdef0123456789 \
  enc.mp4 decrypted.mp4

Then just play the mp4 for flag. They need to hear the audio at the end of the mp4.
