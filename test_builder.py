import json
from app.services.ppt_tool import PresentationBuilder

def test_builder():
    outline = {
        "title": "Test Presentation",
        "slides": [
            {
                "layout": "aesthetic_grid",
                "title": "Test Slide",
                "visual_suggestion": "Bar chart showing test data",
                "bullets": [{"bold": "Test", "text": "This is a test."}],
                "chart_data": {
                    "type": "bar",
                    "labels": ["A", "B", "C"],
                    "values": [10, 20, 30]
                }
            },
            {
                "layout": "aesthetic_metrics",
                "title": "Metrics Slide",
                "visual_suggestion": "Metrics dashboard",
                "metrics": [{"label": "A", "value": "90%"}, {"label": "B", "value": "80%"}],
                "chart_data": {
                    "type": "metrics",
                    "metrics": [{"label": "A", "value": "90%"}, {"label": "B", "value": "80%"}]
                }
            },
            {
                "layout": "aesthetic_split",
                "title": "No Title Test Slide",
                "visual_suggestion": "pie chart",
                "bullets": [{"bold": "Test", "text": "Test"}],
                "chart_data": {
                    "type": "pie",
                    "labels": ["X", "Y"],
                    "values": [50, 50]
                }
            }
        ]
    }
    
    # Simulate an outline with a missing title placeholder by temporarily hacking it inside PresentationBuilder?
    # No, we will just let it run. The bug was already removed.
    
    pb = PresentationBuilder(outline, "test_output.pptx")
    list(pb.build_with_progress())
    print(f"Presentation saved successfully to: test_output.pptx")

if __name__ == "__main__":
    test_builder()
