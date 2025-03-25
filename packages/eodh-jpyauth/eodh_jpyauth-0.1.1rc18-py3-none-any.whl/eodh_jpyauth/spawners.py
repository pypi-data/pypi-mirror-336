from kubespawner.slugs import safe_slug
from kubespawner.spawner import KubeSpawner as KubeSpawner_
from traitlets import Unicode


class KubeSpawner(KubeSpawner_):
    public_url_pattern = Unicode(
        None,
        allow_none=True,
        config=True,
        help="The URL pattern for the public URL",
    )

    async def load_user_options(self):
        """
        Call super method then load workspace from user options. Sets the public URL if
        a pattern is provided.
        """
        await super().load_user_options()
        self.workspace = self.user_options.get("workspace", None)
        if not self.workspace:
            exc = NoWorkspaceSet("No workspace detected in user options.")
            self.log.error("%s", exc)
            raise exc
        self.log.info("Workspace set to '%s'", self.workspace)

        if self.public_url_pattern:
            self.public_url = self._expand_user_properties(self.public_url_pattern)
            self.log.info("Public URL set to '%s'", self.public_url)

    # def get_state(self):
    #     """
    #     Add workspace to the state
    #     """
    #     state = super().get_state()
    #     state["workspace"] = self.workspace
    #     return state

    # def get_env(self):
    #     """
    #     Add workspace to the environment
    #     """
    #     env = super().get_env()
    #     env["WORKSPACE"] = self.workspace
    #     return env

    # def load_state(self, state):
    #     """
    #     Load workspace from state
    #     """
    #     super().load_state(state)
    #     self.workspace = state.get("workspace", None)

    def _options_from_form(self, formdata: dict):
        """
        Add workspace to the user options from the form then call super method and
        return the merged options
        """
        self.log.info("Loading workspace from form data...")
        user_options = dict(workspace=formdata.pop("workspace", [None])[0])
        if not user_options["workspace"]:
            self.log.warning("No workspace detected in form data")
            raise NoWorkspaceSet("No workspace detected in form data.")
        self.log.info("Found workspace '%s' in form data", user_options["workspace"])
        # Merge with the user options from the form
        user_options |= super()._options_from_form(formdata)
        return user_options

    def _expand_user_properties(self, template, slug_scheme=None):
        """
        Expand user properties in template strings
        """
        safe_username = safe_slug(self.user.name)
        safe_workspace = safe_slug(self.workspace)
        safe_servername = safe_slug(self.name or "")
        safe_userserver = (
            f"{safe_username}--{safe_servername}" if safe_servername else safe_username
        )
        ns = dict(
            username=safe_username,
            workspace=safe_workspace,
            servername=safe_servername,
            user_server=safe_userserver,
        )
        for attr_name in ("pod_name", "pvc_name", "namespace"):
            ns[attr_name] = getattr(self, attr_name, f"{attr_name}_unavailable!")
        return template.format(**ns)


class NoWorkspaceSet(Exception):
    pass
