from django_components import component

@component.register("core_test_component")
class CoreTestComponent(component.Component):
    template_name = "core/test_component/test_component.html"

    def get_context_data(self, message="Test OK", status="success"):
        return {
            "message": message,
            "status": status,
        } 