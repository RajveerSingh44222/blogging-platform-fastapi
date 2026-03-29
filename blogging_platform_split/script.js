const API_BASE = "http://127.0.0.1:8000";

// ---------- COMMON HELPERS ----------
function formatDate(dateString) {
  if (!dateString) return "No date";
  return new Date(dateString).toLocaleDateString();
}

function getReadTime(content) {
  if (!content) return "1 min";
  const words = content.trim().split(/\s+/).length;
  return `${Math.max(1, Math.ceil(words / 200))} min`;
}

function showMessage(message, type = "success") {
  const msgBox = document.getElementById("messageBox");
  if (!msgBox) return;

  msgBox.style.display = "block";
  msgBox.textContent = message;
  msgBox.style.background = type === "error" ? "#3a1010" : "#102b18";
  msgBox.style.color = "#fff";

  setTimeout(() => {
    msgBox.style.display = "none";
  }, 2500);
}

// ---------- BLOG CARD HTML ----------
function createBlogCard(blog, showActions = true) {
  return `
    <div class="section-card">
      <div class="post-item-tag">${blog.category}</div>
      <div class="post-item-title">${blog.title}</div>
      <div class="post-item-excerpt">${blog.subtitle || blog.content?.slice(0, 120) || ""}</div>

      <div style="margin-top:12px; color: #aaa; font-size: 14px;">
        By ${blog.author} · ${formatDate(blog.publish_date)} · ${blog.read_time || getReadTime(blog.content)} · ${blog.likes} likes · ${blog.comments_count} comments
      </div>

      ${
        showActions
          ? `
        <div style="margin-top:14px; display:flex; gap:10px; flex-wrap:wrap;">
          <button class="btn-primary" onclick="likeBlog(${blog.id})">Like</button>
          <button class="btn-ghost" onclick="savePost(${blog.id})">Save</button>
          <button class="btn-ghost" onclick="viewComments(${blog.id})">Comments</button>
          <button class="btn-ghost" onclick="openAddComment(${blog.id})">Add Comment</button>
        </div>

        <div id="comment-form-${blog.id}" style="display:none; margin-top:12px;">
          <input type="text" id="commenter-${blog.id}" placeholder="Your name" style="width:100%; padding:10px; margin-bottom:8px;">
          <textarea id="commenttext-${blog.id}" placeholder="Write comment..." style="width:100%; padding:10px; min-height:90px; margin-bottom:8px;"></textarea>
          <button class="btn-primary" onclick="addComment(${blog.id})">Submit Comment</button>
        </div>

        <div id="comments-${blog.id}" style="margin-top:12px;"></div>
      `
          : ""
      }
    </div>
  `;
}

// ---------- INDEX PAGE ----------
async function loadLatestBlogs() {
  const container = document.getElementById("latestBlogs");
  if (!container) return;

  try {
    const response = await fetch(`${API_BASE}/blogs?sort_by=publish_date&order=desc`);
    const blogs = await response.json();

    container.innerHTML = "";

    if (!blogs.length) {
      container.innerHTML = "<p>No blogs available.</p>";
      return;
    }

    container.innerHTML = blogs.slice(0, 6).map(blog => createBlogCard(blog)).join("");
  } catch (error) {
    console.error("Error loading latest blogs:", error);
    container.innerHTML = "<p>Could not load blogs.</p>";
  }
}

// ---------- EXPLORE PAGE ----------
async function loadAllBlogs() {
  const container = document.getElementById("explorePosts");
  if (!container) return;

  try {
    const response = await fetch(`${API_BASE}/blogs`);
    const blogs = await response.json();

    container.innerHTML = "";

    if (!blogs.length) {
      container.innerHTML = "<p>No blogs found.</p>";
      return;
    }

    container.innerHTML = blogs.map(blog => createBlogCard(blog)).join("");
  } catch (error) {
    console.error("Error loading blogs:", error);
    container.innerHTML = "<p>Could not load blogs.</p>";
  }
}

async function searchBlogs() {
  const searchInput = document.getElementById("searchInput");
  const container = document.getElementById("explorePosts");
  if (!searchInput || !container) return;

  const searchValue = searchInput.value.trim();

  try {
    const response = await fetch(`${API_BASE}/blogs?search=${encodeURIComponent(searchValue)}`);
    const blogs = await response.json();

    if (!blogs.length) {
      container.innerHTML = "<p>No matching blogs found.</p>";
      return;
    }

    container.innerHTML = blogs.map(blog => createBlogCard(blog)).join("");
  } catch (error) {
    console.error("Search error:", error);
    container.innerHTML = "<p>Search failed.</p>";
  }
}

async function filterByCategory(category) {
  const container = document.getElementById("explorePosts");
  if (!container) return;

  try {
    const response = await fetch(`${API_BASE}/blogs?category=${encodeURIComponent(category)}`);
    const blogs = await response.json();

    if (!blogs.length) {
      container.innerHTML = `<p>No blogs found in ${category}.</p>`;
      return;
    }

    container.innerHTML = blogs.map(blog => createBlogCard(blog)).join("");
  } catch (error) {
    console.error("Category filter error:", error);
    container.innerHTML = "<p>Could not filter blogs.</p>";
  }
}

// ---------- TAGS PAGE ----------
async function loadTagsPage() {
  const container = document.getElementById("tagResults");
  const tagButtons = document.getElementById("tagButtons");

  if (!container || !tagButtons) return;

  const tagList = ["design", "tech", "culture", "python", "fastapi", "mysql", "react", "writing"];

  tagButtons.innerHTML = tagList.map(tag => `
    <button class="tag-chip" onclick="loadBlogsByTag('${tag}')">#${tag}</button>
  `).join("");

  container.innerHTML = "<p>Select a tag to view blogs.</p>";
}

async function loadBlogsByTag(tag) {
  const container = document.getElementById("tagResults");
  if (!container) return;

  try {
    const response = await fetch(`${API_BASE}/blogs?search=${encodeURIComponent(tag)}`);
    const blogs = await response.json();

    if (!blogs.length) {
      container.innerHTML = `<p>No blogs found for #${tag}</p>`;
      return;
    }

    container.innerHTML = blogs.map(blog => createBlogCard(blog)).join("");
  } catch (error) {
    console.error("Tag fetch error:", error);
    container.innerHTML = "<p>Could not load tag results.</p>";
  }
}

// ---------- WRITE PAGE ----------
async function publishBlog(event) {
  event.preventDefault();

  const title = document.getElementById("blogTitle")?.value.trim();
  const subtitle = document.getElementById("blogSubtitle")?.value.trim();
  const content = document.getElementById("blogContent")?.value.trim();
  const author = document.getElementById("blogAuthor")?.value.trim();
  const category = document.getElementById("blogCategory")?.value;
  const tags = document.getElementById("blogTags")?.value.trim();
  const cover_image = document.getElementById("blogCoverImage")?.value.trim();

  if (!title || !content || !author || !category) {
    showMessage("Please fill all required fields.", "error");
    return;
  }

  const blogData = {
    title,
    subtitle,
    content,
    author,
    category,
    tags,
    cover_image,
    read_time: getReadTime(content),
    is_published: true
  };

  try {
    const response = await fetch(`${API_BASE}/blogs`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(blogData)
    });

    const result = await response.json();

    if (response.ok) {
      showMessage("Blog published successfully.");
      document.getElementById("blogForm").reset();
      setTimeout(() => {
        window.location.href = "explore.html";
      }, 1200);
    } else {
      showMessage(result.detail || "Failed to publish blog.", "error");
    }
  } catch (error) {
    console.error("Publish error:", error);
    showMessage("Something went wrong while publishing.", "error");
  }
}

// ---------- SAVED POSTS ----------
async function savePost(blogId) {
  try {
    const response = await fetch(`${API_BASE}/saved-posts/${blogId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        saved_by: "guest"
      })
    });

    const result = await response.json();

    if (response.ok) {
      showMessage("Post saved successfully.");
    } else {
      showMessage(result.detail || "Could not save post.", "error");
    }
  } catch (error) {
    console.error("Save post error:", error);
    showMessage("Failed to save post.", "error");
  }
}

async function loadSavedPosts() {
  const container = document.getElementById("savedPostsContainer");
  if (!container) return;

  try {
    const savedResponse = await fetch(`${API_BASE}/saved-posts?saved_by=guest`);
    const savedPosts = await savedResponse.json();

    if (!savedPosts.length) {
      container.innerHTML = "<p>No saved posts yet.</p>";
      return;
    }

    const blogPromises = savedPosts.map(item =>
      fetch(`${API_BASE}/blogs/${item.blog_id}`).then(res => res.json())
    );

    const blogs = await Promise.all(blogPromises);

    container.innerHTML = blogs.map(blog => `
      <div class="section-card">
        <div class="post-item-tag">${blog.category}</div>
        <div class="post-item-title">${blog.title}</div>
        <div class="post-item-excerpt">${blog.subtitle || ""}</div>
        <div style="margin-top:10px; color:#aaa;">
          By ${blog.author} · ${formatDate(blog.publish_date)} · ${blog.read_time} · ${blog.likes} likes · ${blog.comments_count} comments
        </div>
        <div style="margin-top:12px;">
          <button class="btn-ghost" onclick="removeSavedPost(${blog.id})">Remove</button>
        </div>
      </div>
    `).join("");
  } catch (error) {
    console.error("Load saved posts error:", error);
    container.innerHTML = "<p>Failed to load saved posts.</p>";
  }
}

async function removeSavedPost(blogId) {
  try {
    const response = await fetch(`${API_BASE}/saved-posts/${blogId}?saved_by=guest`, {
      method: "DELETE"
    });

    const result = await response.json();

    if (response.ok) {
      showMessage("Saved post removed.");
      loadSavedPosts();
    } else {
      showMessage(result.detail || "Could not remove saved post.", "error");
    }
  } catch (error) {
    console.error("Remove saved post error:", error);
    showMessage("Failed to remove saved post.", "error");
  }
}

// ---------- LIKES ----------
async function likeBlog(blogId) {
  try {
    const response = await fetch(`${API_BASE}/blogs/${blogId}/like`, {
      method: "POST"
    });

    const result = await response.json();

    if (response.ok) {
      showMessage(`Liked. Total likes: ${result.total_likes}`);
      if (document.getElementById("explorePosts")) loadAllBlogs();
      if (document.getElementById("latestBlogs")) loadLatestBlogs();
      if (document.getElementById("tagResults")) {
        const currentTagBtn = document.querySelector(".tag-chip.active");
        if (currentTagBtn) currentTagBtn.click();
      }
    } else {
      showMessage(result.detail || "Failed to like post.", "error");
    }
  } catch (error) {
    console.error("Like error:", error);
    showMessage("Like request failed.", "error");
  }
}

// ---------- COMMENTS ----------
function openAddComment(blogId) {
  const form = document.getElementById(`comment-form-${blogId}`);
  if (!form) return;
  form.style.display = form.style.display === "none" ? "block" : "none";
}

async function addComment(blogId) {
  const commenterInput = document.getElementById(`commenter-${blogId}`);
  const commentTextInput = document.getElementById(`commenttext-${blogId}`);

  const commenter_name = commenterInput?.value.trim();
  const comment_text = commentTextInput?.value.trim();

  if (!commenter_name || !comment_text) {
    showMessage("Fill both name and comment.", "error");
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/blogs/${blogId}/comments`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        commenter_name,
        comment_text
      })
    });

    const result = await response.json();

    if (response.ok) {
      showMessage("Comment added.");
      commenterInput.value = "";
      commentTextInput.value = "";
      viewComments(blogId);

      if (document.getElementById("explorePosts")) loadAllBlogs();
      if (document.getElementById("latestBlogs")) loadLatestBlogs();
    } else {
      showMessage(result.detail || "Could not add comment.", "error");
    }
  } catch (error) {
    console.error("Comment error:", error);
    showMessage("Comment request failed.", "error");
  }
}

async function viewComments(blogId) {
  const container = document.getElementById(`comments-${blogId}`);
  if (!container) return;

  try {
    const response = await fetch(`${API_BASE}/blogs/${blogId}/comments`);
    const comments = await response.json();

    if (!comments.length) {
      container.innerHTML = "<p style='margin-top:10px;'>No comments yet.</p>";
      return;
    }

    container.innerHTML = comments.map(comment => `
      <div style="margin-top:10px; padding:10px; border:1px solid #333; border-radius:8px;">
        <strong>${comment.commenter_name}</strong>
        <div style="font-size:13px; color:#aaa;">${formatDate(comment.created_at)}</div>
        <p style="margin-top:6px;">${comment.comment_text}</p>
      </div>
    `).join("");
  } catch (error) {
    console.error("View comments error:", error);
    container.innerHTML = "<p>Could not load comments.</p>";
  }
}