import gradio as gr


class UISettings:
    """
    Utility class for managing UI settings.

    This class provides static methods for toggling UI components, such as a sidebar.
    """
    @staticmethod
    def toggle_sidebar(state):
        """
        Toggle the visibility state of a UI component.

    
        """
        state = not state
        return gr.update(visible=state), state

    @staticmethod
    def feedback(data: gr.LikeData):
        """
        Process user feedback on the generated response.

        """
        if data.liked:
            print("You upvoted this response: " + data.value)
        else:
            print("You downvoted this response: " + data.value)