from __future__ import annotations

from django import forms
from django.shortcuts import redirect
from django_control_components.infolists import Infolist, TextEntry, BadgeEntry
from django_control_components.schemas import Schema, Section, TextInput, Select, Toggle
from django_control_components.wizards import WizardStep, WizardView


class ProjectDetailsForm(forms.Form):
    name = forms.CharField(max_length=100, label="Project Name", required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False)


class ProjectSettingsForm(forms.Form):
    tier = forms.ChoiceField(
        choices=[("starter", "Starter Plan"), ("pro", "Professional Plan"), ("enterprise", "Enterprise")],
        initial="pro",
        label="Subscription Tier",
    )
    is_public = forms.BooleanField(required=False, initial=True, label="Publicly Discoverable")


class LiveWizardDemoView(WizardView):
    wizard_class = "demo-live-wizard"
    show_step_nav = True

    steps_config = [
        WizardStep(
            "details",
            Schema.make()
            .form(ProjectDetailsForm)
            .strict()
            .schema([
                Section.make("Project Information")
                .description("Basic project identifiers")
                .schema([
                    TextInput.make("name").required(),
                    TextInput.make("description"),
                ]),
            ]),
            title="Details",
            heading="Project Basics",
            description="Enter the core parameters for the new project.",
        ),
        WizardStep(
            "settings",
            Schema.make()
            .form(ProjectSettingsForm)
            .strict()
            .schema([
                Section.make("Configuration")
                .columns(2)
                .schema([
                    Select.make("tier").searchable(),
                    Toggle.make("is_public"),
                ]),
            ]),
            title="Plan & Privacy",
            heading="Settings",
            description="Select subscription level and public visibility.",
        ),
        WizardStep(
            "review",
            Infolist.make().schema([
                TextEntry.make("name").label("Project Name"),
                BadgeEntry.make("tier").label("Selected Tier").colors({
                    "starter": "muted",
                    "pro": "primary",
                    "enterprise": "success",
                }),
                TextEntry.make("is_public").label("Public Access"),
            ]),
            title="Review",
            heading="Review & Confirm",
            description="Review the entered data before submission.",
            record=lambda view: view.get_all_cleaned_data(),
        ),
    ]

    def done(self, form_list, **kwargs):
        return redirect("dcc-panel-docs:page-wizards")
