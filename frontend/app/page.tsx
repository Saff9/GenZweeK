// frontend/app/page.tsx
"use client";

import { useEffect, useState } from "react";

type Post = {
  id: number;
  user_id: number;
  text: string;
  media_type: "none" | "image" | "video";
  media_file?: string;
  like_count: number;
  comment_count: number;
  view_count: number;
  created_at: string;
  is_expired: boolean;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api";

export default function HomePage() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [text, setText] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [fileError, setFileError] = useState<string | null>(null);

  useEffect(() => {
    loadPosts();
  }, []);

  async function loadPosts() {
    try {
      setLoading(true);
      setError(null);
      const res = await fetch(`${API_BASE}/posts/`);
      if (!res.ok) throw new Error("Failed to load posts");
      const data = await res.json();
      setPosts(data);
    } catch (err: any) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0] || null;
    setFile(file);
    setFileError(null);
    
    if (!file) return;

    const sizeMB = file.size / (1024 * 1024);
    const isImage = file.type.startsWith("image/");
    const isVideo = file.type.startsWith("video/");

    if (isImage && sizeMB > 10) {
      setFileError("Image too large (max 10 MB). Try compressing.");
      setFile(null);
    } else if (isVideo && sizeMB > 50) {
      setFileError("Video too large (max 50 MB). Try shorter clip.");
      setFile(null);
    } else if (!isImage && !isVideo) {
      setFileError("Only images (JPEG/PNG) or videos (MP4) allowed.");
      setFile(null);
    }
  }

  async function handleCreatePost(e: React.FormEvent) {
    e.preventDefault();
    if (!text.trim()) {
      setError("Text is required for posts.");
      return;
    }

    try {
      setError(null);
      const formData = new FormData();
      formData.append("text", text.trim());
      
      if (file) {
        formData.append("media_file", file);
        formData.append("media_type", 
          file.type.startsWith("image/") ? "image" : "video"
        );
      } else {
        formData.append("media_type", "none");
      }

      const res = await fetch(`${API_BASE}/posts/`, {
        method: "POST",
        credentials: "include",
        body: formData,
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.detail || data[0]?.[0] || "Failed to create post");
      }

      const newPost: Post = await res.json();
      setPosts([newPost, ...posts]);
      setText("");
      setFile(null);
      (e.target as any).reset();
    } catch (err: any) {
      setError(err.message || "Failed to create post");
    }
  }

  if (loading) {
    return <div className="text-center py-12 text-slate-400">Loading GenZweeK...</div>;
  }

  return (
    <div className="space-y-4">
      <form onSubmit={handleCreatePost} className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur p-4 space-y-3">
        <textarea
          className="w-full bg-transparent text-lg outline-none resize-none min-h-[80px] placeholder:text-slate-400"
          placeholder="What's happening this week? 📝 Text-first posts get priority!"
          value={text}
          onChange={(e) => setText(e.target.value)}
          maxLength={2000}
        />
        <div className="flex items-center justify-between gap-3 pt-1">
          <label className="flex items-center gap-2 text-sm text-slate-300 bg-white/5 px-3 py-2 rounded-xl cursor-pointer hover:bg-white/10 transition-all">
            📎 Attach media
            <input type="file" className="hidden" accept="image/*,video/*" onChange={handleFileChange} />
          </label>
          <button
            type="submit"
            disabled={!text.trim()}
            className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 text-sm font-bold shadow-lg hover:shadow-xl transition-all disabled:opacity-50 disabled:from-gray-500"
          >
            Post
          </button>
        </div>
        {file && (
          <p className="text-xs text-slate-300 truncate">
            ✅ {file.name} ({(file.size / 1024 / 1024).toFixed(1)} MB)
          </p>
        )}
        {fileError && (
          <p className="text-xs text-red-400 bg-red-500/10 p-2 rounded-lg">{fileError}</p>
        )}
      </form>

      {error && (
        <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-2xl text-red-300 text-sm">
          {error}
        </div>
      )}

      {posts.length === 0 ? (
        <div className="text-center py-16 text-slate-400">
          <div className="text-4xl mb-4">✨</div>
          <p>Be the first to share your week!</p>
        </div>
      ) : (
        <div className="space-y-3">
          {posts.map((post) => (
            <article key={post.id} className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur p-4 space-y-3 hover:border-white/20 transition-all">
              <p className="text-base leading-relaxed whitespace-pre-wrap">{post.text}</p>
              {post.media_type !== "none" && post.media_file && (
                <div className="rounded-xl overflow-hidden border border-white/10">
                  {post.media_type === "image" ? (
                    <img src={post.media_file} alt="" className="w-full h-64 object-cover" />
                  ) : (
                    <video src={post.media_file} className="w-full h-64 object-cover" controls />
                  )}
                </div>
              )}
              <div className="flex items-center gap-4 text-xs text-slate-400 pt-1">
                <span>❤️ {post.like_count}</span>
                <span>💬 {post.comment_count}</span>
                <span>👁️ {post.view_count}</span>
              </div>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}
