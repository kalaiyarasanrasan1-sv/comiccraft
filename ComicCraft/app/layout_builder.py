def build_comic_layout(outline, story, image_paths):
    story_by_panel = {p.panel_number: p for p in story.panels}
    layout = []
    for panel in outline.panels:
        s = story_by_panel.get(panel.panel_number)
        layout.append({
            "panel_number": panel.panel_number,
            "title": panel.title,
            "scene_description": panel.scene_description,
            "image_prompt": panel.image_prompt,
            "image_path": image_paths[panel.panel_number - 1],
            "caption": s.caption if s else "",
            "narration": s.narration if s else "",
            "dialogue": s.dialogue if s else "",
        })
    return layout
