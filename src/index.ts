// dain.ts
import { exec } from 'child_process';
// import { uploadToYouTubeShorts } from './api/YouTube/upload';
// import { uploadToInstagramReels } from './api/Instagram/upload';
import path from 'path';

// Reusable metadata
const post = {
  title: "Just dev things 💻",
  description: "Caught in another infinite loop.",
  hashtags: ['coding', 'shorts', 'tiktok', 'funny'],
  videoPath: './videos/my_video.mp4',
};

const formatCaption = () => {
  return `${post.title}\n\n${post.description}\n\n${post.hashtags.map(h => `#${h}`).join(' ')}`;
};

const uploadToTikTok = async (): Promise<void> => {
  const absolutePath = path.resolve(post.videoPath);
  const caption = formatCaption();

  return new Promise((resolve, reject) => {
    exec(`python3 ./api/TikTok/main.py "${absolutePath}" "${caption}"`, (err, stdout, stderr) => {
      if (err) {
        console.error('[TikTok] Error:', stderr);
        return reject(err);
      }
      console.log('[TikTok] Success:', stdout);
      resolve();
    });
  });
};

(async () => {
  const caption = formatCaption();

  try {
    console.log('[DAIN] Uploading to TikTok...');
    await uploadToTikTok();
  } catch {}

  try {
    console.log('[DAIN] Uploading to YouTube Shorts...');
    await uploadToYouTubeShorts(post.videoPath, post.title, post.description, post.hashtags);
  } catch (e) {
    console.error('[YouTube Shorts] Error:', e);
  }

  try {
    console.log('[DAIN] Uploading to Instagram Reels...');
    await uploadToInstagramReels(post.videoPath, caption);
  } catch (e) {
    console.error('[Instagram Reels] Error:', e);
  }
})();