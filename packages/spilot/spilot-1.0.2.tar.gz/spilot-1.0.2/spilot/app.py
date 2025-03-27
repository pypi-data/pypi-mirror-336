"""
Textual TUI application for Slurm job handling
"""

import subprocess
import shutil
import os
import getpass
from datetime import datetime
from typing import List, Dict, Any, Optional

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.widgets import Header, Footer, DataTable, Static, Input, Button, Select
from textual.reactive import reactive
from textual.coordinate import Coordinate
from textual.timer import Timer
from textual.binding import Binding, BindingsMap

DELIMITER = chr(0xE000)

# Compatibility for Python 3.8


def remove_suffix(text: str, suffix: str) -> str:
    if text.endswith(suffix):
        return text[: -len(suffix)]
    return text


class SlurmInfo:
    """Class to handle Slurm job information retrieval"""

    @staticmethod
    def is_slurm_available() -> bool:
        """Check if Slurm is available on the system"""
        return shutil.which("squeue") is not None

    @staticmethod
    def get_slurm_jobs() -> List[Dict[str, Any]]:
        """Get information about running Slurm jobs"""
        if not SlurmInfo.is_slurm_available():
            return []

        try:
            # Run squeue with format specifiers to get job details
            cmd = [
                "squeue",
                f"--format=%i{DELIMITER}%j{DELIMITER}%u{DELIMITER}%P{DELIMITER}%T{DELIMITER}%M{DELIMITER}%l{DELIMITER}%D{DELIMITER}%r{DELIMITER}%S{DELIMITER}%p",
                "--noheader",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            jobs = []
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue

                # Parse job data
                parts = line.split(DELIMITER)
                if len(parts) >= 11:
                    (
                        job_id,
                        name,
                        user,
                        partition,
                        state,
                        time,
                        time_limit,
                        nodes,
                        reason,
                        start_time,
                        priority,
                    ) = parts[:11]
                else:
                    continue

                jobs.append(
                    {
                        "id": int(job_id),
                        "name": str(name),
                        "user": str(user),
                        "partition": str(partition),
                        "state": str(state),
                        "time": str(time),
                        "time_limit": str(time_limit),
                        "nodes": str(nodes),
                        "reason": str(reason),
                        "start_time": str(start_time),
                        "priority": str(priority),
                    }
                )
            return jobs
        except subprocess.CalledProcessError:
            return []
        except Exception as e:
            # Fallback for any unexpected errors
            print(f"Error getting Slurm jobs: {e}")
            return []

    @staticmethod
    def get_job_details(job_id: str) -> Dict[str, str]:
        """Get detailed information about a specific Slurm job"""
        if not SlurmInfo.is_slurm_available():
            return {}

        try:
            # Run scontrol to get detailed job information
            cmd = ["scontrol", "show", "job", str(job_id)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            # Parse the output into a dictionary
            details = {}
            for line in result.stdout.strip().split("\n"):
                line = line.strip()
                if not line:
                    continue

                # Split by spaces and equals signs
                parts = line.split()
                for part in parts:
                    if "=" in part:
                        key, value = part.split("=", 1)
                        details[key] = value

            return details
        except (subprocess.CalledProcessError, Exception) as e:
            return {}

    @staticmethod
    def get_partition_details(partition_name: str) -> Dict[str, str]:
        """Get detailed information about a specific Slurm partition"""
        if not SlurmInfo.is_slurm_available():
            return {}

        partition_name = remove_suffix(partition_name, "*")

        try:
            # Run scontrol to get detailed partition information
            cmd = ["scontrol", "show", "partition", str(partition_name)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            # Parse the output into a dictionary
            details = {}
            for line in result.stdout.strip().split("\n"):
                line = line.strip()
                if not line:
                    continue

                # Split by spaces and equals signs
                parts = line.split()
                for part in parts:
                    if "=" in part:
                        key, value = part.split("=", 1)
                        details[key] = value

            return details
        except (subprocess.CalledProcessError, Exception) as e:
            return {}

    @staticmethod
    def get_node_details(node_name: str) -> Dict[str, str]:
        """Get detailed information about a specific Slurm node"""
        if not SlurmInfo.is_slurm_available():
            return {}

        try:
            # Run scontrol to get detailed node information
            cmd = ["scontrol", "show", "node", str(node_name)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            # Parse the output into a dictionary
            details = {}
            for line in result.stdout.strip().split("\n"):
                line = line.strip()
                if not line:
                    continue

                # Split by spaces and equals signs
                parts = line.split()
                for part in parts:
                    if "=" in part:
                        key, value = part.split("=", 1)
                        details[key] = value

            return details
        except (subprocess.CalledProcessError, Exception) as e:
            return {}


class SlurmNotAvailableBanner(Static):
    """Banner widget to display when Slurm is not available"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.styles.padding = (2, 4)
        self.styles.background = "red"
        self.styles.color = "white"
        self.styles.text_align = "center"
        self.update(
            "[b]Slurm is not installed![/b]\n\nspilot is built for HPC systems running Slurm."
        )


class JobDetailsPanel(Static):
    """Panel to display detailed information about a selected job"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.styles.border = ("heavy", "white")
        self.styles.padding = (1, 2)
        self.current_job_id = None

    def update_job_details(self, job_id: str):
        """Update the panel with details for the specified job"""
        if not job_id or job_id == self.current_job_id:
            return

        self.current_job_id = job_id
        details = SlurmInfo.get_job_details(job_id)

        if not details:
            self.update(
                f"[b][u]Job Details for {job_id}[/u][/b]\n\n[i]No details available[/i]"
            )
            return

        # Start with the header
        content = f"[b][u]Job Details for {job_id}[/u][/b]\n\n"

        # Add important details first in a more structured way
        important_keys = [
            "JobId",
            "JobName",
            "UserId",
            "Partition",
            "State",
            "RunTime",
            "TimeLimit",
            "NumNodes",
            "NumCPUs",
            "Reason",
            "Priority",
            "Command",
            "WorkDir",
        ]

        content += "[b][u]Important Details:[/u][/b] \n"
        for key in important_keys:
            if key in details:
                content += f"· [b]{key}:[/b] [green]{details[key].replace('[','(').replace(']',')')}[/green]\n"

        # Add a visual separator for clarity
        content += "\n[b][u]Additional Information:[/u][/b] \n"

        # Add the rest of the details
        for key, value in details.items():
            if key not in important_keys:
                content += f"· [b]{key}:[/b] [green]{value.replace('[','(').replace(']',')')}[/green]\n"

        # Final update with the beautified content
        self.update(content)


class SlurmJobsView(Container):
    """Main container for Slurm jobs display"""

    jobs = reactive([])
    last_updated = reactive(datetime.now())
    cursor_job_id = 0
    refresh_timer: Optional[Timer] = None
    columns = {
        "id": [int, "Job ID", 8, ">"],
        "name": [str, "Name", 16, "^"],
        "user": [str, "User", 12, "^"],
        "state": [str, "State", 0, "^"],
        "time": [str, "Runtime", 12, ">"],
        "time_limit": [str, "Time Limit", 12, ">"],
        "partition": [str, "Partition", 10, "^"],
        "nodes": [str, "Nodes", 0, "^"],
        "reason": [str, "Reason", 0, "^"],
        "start_time": [str, "Start Time", 0, "^"],
        "priority": [str, "Priority", 0, "^"],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table = DataTable(zebra_stripes=True)
        self.status_message = Static("")
        self.details_panel = JobDetailsPanel()
        self.current_username = self._get_current_username()

    def _get_current_username(self) -> str:
        """Get the current username"""
        try:
            return getpass.getuser()
        except Exception:
            try:
                return os.getlogin()
            except Exception:
                return ""

    def compose(self) -> ComposeResult:
        """Compose the job view widget with horizontal split"""
        yield self.status_message

        with Horizontal():
            left_container = Vertical()
            left_container.styles.width = "50%"
            left_container.styles.height = "100%"
            left_container.border_title = "Current Jobs"
            left_container.styles.border = ("heavy", "white")

            with left_container:
                yield self.table

            right_container = VerticalScroll(can_focus=True, can_focus_children=True)
            right_container.styles.width = "50%"
            right_container.styles.height = "100%"

            with right_container:
                yield self.details_panel

    def on_mount(self) -> None:
        """Set up the widget when mounted"""
        for key, [_, heading, width, _] in self.columns.items():
            if width > 0:
                self.table.add_column(heading.center(width), width=width)

        # Configure the cursor to move row-wise
        self.table.cursor_type = "row"

        # Start the refresh timer
        self.refresh_jobs()

    def on_data_table_row_highlighted(self, event) -> None:
        """Handle row highlight events to update the details panel"""
        row_index = event.cursor_row
        if 0 <= row_index < len(self.jobs):
            self.cursor_job_id = self.jobs[row_index]["id"]
            self.details_panel.update_job_details(self.cursor_job_id)

    def refresh_jobs(self) -> None:
        """Refresh the job list"""
        raw_jobs = SlurmInfo.get_slurm_jobs()
        self.last_updated = datetime.now()

        # Sort jobs according to requirements:
        # 1. Current user's jobs first
        # 2. Other users' running jobs
        # 3. Other users' pending jobs
        sorted_jobs = []

        # Current user's jobs (any state)
        current_user_jobs = sorted(
            [job for job in raw_jobs if job["user"] == self.current_username],
            key=lambda j: j["id"],
        )
        sorted_jobs.extend(current_user_jobs)

        # Other users' running jobs
        other_running_jobs = sorted(
            [
                job
                for job in raw_jobs
                if job["user"] != self.current_username and job["state"] == "RUNNING"
            ],
            key=lambda j: j["id"],
        )
        sorted_jobs.extend(other_running_jobs)

        # Other users' pending jobs
        other_pending_jobs = sorted(
            [
                job
                for job in raw_jobs
                if job["user"] != self.current_username and job["state"] != "RUNNING"
            ],
            key=lambda j: j["id"],
        )
        sorted_jobs.extend(other_pending_jobs)

        self.jobs = sorted_jobs

        # Update the table data
        self.table.clear()

        for i, job in enumerate(self.jobs):
            # Add the row with a key based on index
            row_key = f"job-{i}"
            state = job["state"]
            reason = job["reason"]

            # Apply styling based on job state
            if state == "RUNNING":
                style = "bold green"
            elif state == "PENDING" and reason == "Priority":
                style = "bold white"
                job["time"] = job["reason"]
            elif state == "PENDING":
                job["time"] = job["reason"]
                style = "bold red"

            row = [
                f"[{style}]{job[key]:{align}{width}}[/{style}]"
                for key, [_, _, width, align] in self.columns.items()
                if width > 0
            ]

            self.table.add_row(*row, key=row_key)

        self.status_message.update(
            f"Last updated: {self.last_updated.strftime('%Y-%m-%d %H:%M:%S')} ({len(self.jobs)} jobs found)"
        )

        # Select the first row if there are jobs
        if self.jobs and self.table.row_count > 0:
            try:
                self.table.cursor_coordinate = Coordinate(
                    [job["id"] for job in self.jobs].index(self.cursor_job_id), 0
                )
            except Exception as e:
                self.table.cursor_coordinate = Coordinate(0, 0)
            self.details_panel.update_job_details(
                str(self.jobs[self.table.cursor_row]["id"])
            )

        if self.refresh_timer:
            self.refresh_timer.stop()

        self.refresh_timer = self.set_interval(10, self.refresh_jobs, repeat=1)


class HardwareDetailsPanel(Static):
    """Panel to display detailed information about a selected partition or node"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.styles.border = ("heavy", "white")
        self.styles.padding = (1, 2)
        self.current_resource_id = None
        self.current_resource_type = None

    def update_partition_details(self, partition_name: str):
        """Update the panel with details for the specified partition"""
        if not partition_name or (
            self.current_resource_id == partition_name
            and self.current_resource_type == "partition"
        ):
            return

        self.current_resource_id = partition_name
        self.current_resource_type = "partition"
        details = SlurmInfo.get_partition_details(partition_name)

        if not details:
            self.update(
                f"[b][u]Partition Details for {remove_suffix(partition_name, '*')}[/u][/b]\n\n[i]No details available[/i]"
            )
            return

        # Start with the header
        content = f"[b][u]Partition Details for {remove_suffix(partition_name, '*')}[/u][/b]\n\n"

        # Add important details first in a more structured way
        important_keys = [
            "PartitionName",
            "Nodes",
            "State",
            "MaxTime",
            "DefaultTime",
            "MaxNodes",
            "MinNodes",
            "Priority",
            "DefaultQOS",
            "PreemptMode",
        ]

        content += "[b][u]Important Details:[/u][/b] \n"
        for key in important_keys:
            if key in details:
                content += f"· [b]{key}:[/b] [green]{details[key].replace('[','(').replace(']',')')}[/green]\n"

        # Add a visual separator for clarity
        content += "\n[b][u]Additional Information:[/u][/b] \n"

        # Add the rest of the details
        for key, value in details.items():
            if key not in important_keys:
                content += f"· [b]{key}:[/b] [green]{value.replace('[','(').replace(']',')')}[/green]\n"

        # Final update with the beautified content
        self.update(content)

    def update_node_details(self, node_name: str):
        """Update the panel with details for the specified node"""
        if not node_name or (
            self.current_resource_id == node_name
            and self.current_resource_type == "node"
        ):
            return

        self.current_resource_id = node_name
        self.current_resource_type = "node"
        details = SlurmInfo.get_node_details(node_name)

        if not details:
            self.update(
                f"[b][u]Node Details for {node_name}[/u][/b]\n\n[i]No details available[/i]"
            )
            return

        # Start with the header
        content = f"[b][u]Node Details for {node_name}[/u][/b]\n\n"

        # Add important details first in a more structured way
        important_keys = [
            "NodeName",
            "Partitions",
            "State",
            "CPUs",
            "CPULoad",
            "RealMemory",
            "AllocMemory",
            "FreeMem",
            "Sockets",
            "Cores",
            "ThreadsPerCore",
            "Gres",
            "ActiveFeatures",
            "AvailableFeatures",
        ]

        content += "[b][u]Important Details:[/u][/b] \n"
        for key in important_keys:
            if key in details:
                content += f"· [b]{key}:[/b] [green]{details[key].replace('[','(').replace(']',')')}[/green]\n"

        # Add a visual separator for clarity
        content += "\n[b][u]Additional Information:[/u][/b] \n"

        # Add the rest of the details
        for key, value in details.items():
            if key not in important_keys:
                content += f"· [b]{key}:[/b] [green]{value.replace('[','(').replace(']',')')}[/green]\n"

        # Final update with the beautified content
        self.update(content)


# Now replace the HardwareConfigView class with this updated version:


class HardwareConfigView(Container):
    """View to display hardware configuration and status of Slurm partitions and nodes"""

    partitions = reactive([])
    nodes = reactive([])
    last_updated = reactive(datetime.now())
    refresh_timer: Optional[Timer] = None
    cursor_partition_name = None
    cursor_node_name = None

    # Define columns with data type, heading, width, and alignment
    partition_columns = {
        "name": [str, "Name", 12, "<"],
        "state": [str, "State", 10, "^"],
        "nodes": [str, "Nodes", 10, "^"],
        "avail": [str, "Avail", 8, "^"],
        "cpus": [str, "CPUs", 8, ">"],
        "time_limit": [str, "Time Limit", 15, "^"],
        "memory": [str, "Memory", 15, ">"],
    }

    node_columns = {
        "name": [str, "Name", 12, "<"],
        "partition": [str, "Partition", 12, "<"],
        "state": [str, "State", 12, "^"],
        "cpus": [str, "CPUs", 8, ">"],
        "load": [str, "Load", 10, ">"],
        "memory": [str, "Memory", 15, ">"],
        "usage": [str, "Usage", 10, "^"],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.partition_table = DataTable(id="partition-table", zebra_stripes=True)
        self.node_table = DataTable(id="node-table", zebra_stripes=True)
        self.status_message = Static("")
        self.details_panel = HardwareDetailsPanel()

    def compose(self) -> ComposeResult:
        """Compose the hardware view widget with horizontal split for tables and details"""
        yield self.status_message

        with Horizontal():
            # Left column with partitions and nodes
            left_column = Vertical()
            left_column.styles.width = "50%"
            left_column.styles.height = "100%"

            with left_column:
                # Partition section
                partition_container = Container()
                partition_container.border_title = "Partitions"
                partition_container.styles.border = ("heavy", "white")
                partition_container.styles.height = "30%"

                with partition_container:
                    yield self.partition_table

                # Node section
                node_container = Container()
                node_container.border_title = "Nodes"
                node_container.styles.border = ("heavy", "white")
                node_container.styles.height = "70%"

                with node_container:
                    yield self.node_table

            # Right column with details panel
            right_column = VerticalScroll(can_focus=True, can_focus_children=True)
            right_column.styles.width = "50%"
            right_column.styles.height = "100%"

            with right_column:
                yield self.details_panel

    def on_mount(self) -> None:
        """Set up the widget when mounted"""
        self.partition_table.cursor_type = "row"
        self.node_table.cursor_type = "row"

        # Configure partition table columns
        for key, [_, heading, width, _] in self.partition_columns.items():
            if width > 0:
                self.partition_table.add_column(heading.center(width), width=width)

        # Configure node table columns
        for key, [_, heading, width, _] in self.node_columns.items():
            if width > 0:
                self.node_table.add_column(heading.center(width), width=width)

        # Start the refresh timer
        self.refresh_hardware_info()

    def on_data_table_row_highlighted(self, event) -> None:
        """Handle row highlight events to update the details panel"""
        table = event.data_table
        row_index = event.cursor_row

        # Update the appropriate details based on which table was interacted with
        if table.id == "partition-table" and 0 <= row_index < len(self.partitions):
            partition_name = self.partitions[row_index]["name"]
            self.cursor_partition_name = partition_name
            self.details_panel.update_partition_details(partition_name)
        elif table.id == "node-table" and 0 <= row_index < len(self.nodes):
            node_name = self.nodes[row_index]["name"]
            self.cursor_node_name = node_name
            self.details_panel.update_node_details(node_name)

    def refresh_hardware_info(self) -> None:
        """Refresh the partition and node information"""
        self.refresh_partitions()
        self.refresh_nodes()
        self.last_updated = datetime.now()
        self.status_message.update(
            f"Last updated: {self.last_updated.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        if self.refresh_timer:
            self.refresh_timer.stop()

        self.refresh_timer = self.set_interval(30, self.refresh_hardware_info, repeat=1)

    def refresh_partitions(self) -> None:
        """Refresh the partition information"""
        if not SlurmInfo.is_slurm_available():
            return

        try:
            # Get partition information using sinfo
            cmd = [
                "sinfo",
                f"--format=%P{DELIMITER}%a{DELIMITER}%D{DELIMITER}%T{DELIMITER}%c{DELIMITER}%l{DELIMITER}%m",
                "--noheader",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            partitions = []
            self.partition_table.clear()

            for i, line in enumerate(result.stdout.strip().split("\n")):
                if not line:
                    continue

                parts = line.split(DELIMITER)
                if len(parts) >= 7:
                    name, avail, nodes, state, cpus, time_limit, memory = parts

                    partition = {
                        "name": name.strip(),
                        "avail": avail.strip(),
                        "nodes": nodes.strip(),
                        "state": state.strip(),
                        "cpus": cpus.strip(),
                        "time_limit": time_limit.strip(),
                        "memory": memory.strip(),
                    }
                    partitions.append(partition)

                    # Determine row style based on partition state
                    state_lower = state.strip().lower()
                    if "down" in state_lower:
                        style = "bold red"
                    elif "up" in state_lower:
                        style = "bold green"
                    elif "mix" in state_lower:
                        style = "bold white"
                    else:
                        style = "bold yellow"

                    # Format each cell with proper width and alignment
                    row = [
                        f"[{style}]{partition[key]:{align}{width}}[/{style}]"
                        for key, [_, _, width, align] in self.partition_columns.items()
                        if width > 0
                    ]

                    # Use index to ensure unique keys
                    self.partition_table.add_row(*row, key=f"partition-{i}")

            self.partitions = partitions

            # Restore cursor position for partitions
            if partitions:
                try:
                    if self.cursor_partition_name:
                        # Find the partition index with the saved name
                        for i, partition in enumerate(partitions):
                            if partition["name"] == self.cursor_partition_name:
                                self.partition_table.cursor_coordinate = Coordinate(
                                    i, 0
                                )
                                break
                except Exception:
                    pass

                # Select the first partition if no current selection
                if not self.details_panel.current_resource_id:
                    self.details_panel.update_partition_details(partitions[0]["name"])

        except Exception as e:
            self.partition_table.clear()
            self.partition_table.add_row(
                "Error retrieving partition data", str(e), "", "", "", "", ""
            )

    def refresh_nodes(self) -> None:
        """Refresh the node information"""
        if not SlurmInfo.is_slurm_available():
            return

        try:
            # Get node information using sinfo
            cmd = [
                "sinfo",
                "--Node",
                f"--format=%N{DELIMITER}%P{DELIMITER}%t{DELIMITER}%c{DELIMITER}%O{DELIMITER}%m{DELIMITER}%T",
                "--noheader",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            nodes = []
            self.node_table.clear()

            for i, line in enumerate(result.stdout.strip().split("\n")):
                if not line:
                    continue

                parts = line.split(DELIMITER)
                if len(parts) >= 7:
                    name, partition, state, cpus, load, memory, usage = parts

                    node = {
                        "name": name.strip(),
                        "partition": partition.strip(),
                        "state": state.strip(),
                        "cpus": cpus.strip(),
                        "load": load.strip(),
                        "memory": memory.strip(),
                        "usage": usage.strip(),
                    }
                    nodes.append(node)

                    # Determine row style based on node state
                    state_lower = state.strip().lower()
                    if state_lower == "idle":
                        style = "bold green"
                    elif state_lower in ["down", "drain", "fail", "alloc"]:
                        style = "bold red"
                    elif state_lower == "mix":
                        style = "bold white"
                    else:
                        style = "bold yellow"

                    # Format each cell with proper width and alignment
                    row = [
                        f"[{style}]{node[key]:{align}{width}}[/{style}]"
                        for key, [_, _, width, align] in self.node_columns.items()
                        if width > 0
                    ]

                    # Use index to ensure unique keys
                    self.node_table.add_row(*row, key=f"node-{i}")

            self.nodes = nodes

            # Restore cursor position for nodes
            if nodes:
                try:
                    if self.cursor_node_name:
                        # Find the node index with the saved name
                        for i, node in enumerate(nodes):
                            if node["name"] == self.cursor_node_name:
                                self.node_table.cursor_coordinate = Coordinate(i, 0)
                                break
                except Exception:
                    pass
        except Exception as e:
            self.node_table.clear()
            self.node_table.add_row(
                "Error retrieving node data", str(e), "", "", "", "", ""
            )


class JobSubmitterView(Container):
    """View to configure and submit Slurm jobs"""

    partitions = reactive([])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_message = Static("")
        self.submit_status = Static("")
        self.submit_status.styles.margin = (1, 0)
        self.working_dir = os.getcwd()

    def compose(self) -> ComposeResult:
        """Compose the job submitter view with form inputs"""
        yield self.status_message

        form_scroller = VerticalScroll(id="form_scroll", can_focus=True)
        form_scroller.styles.border = ("heavy", "white")
        form_scroller.border_title = "Submit a Job"
        form_scroller.styles.width = "100%"
        form_scroller.styles.height = "100%"
        form_scroller.styles.padding = (1, 2)

        with form_scroller:
            # Job name
            yield Static("Job Name:")
            yield Input(placeholder="Enter job name", id="job_name")

            # Partition selection
            yield Static("Partition:")
            yield Select(
                [("null", "CPU"), ("null2", "GPU")], id="partition", allow_blank=False
            )

            # Node count
            yield Static("Number of Nodes:")
            yield Input(placeholder="1", id="nodes", value="1")

            # CPU count
            yield Static("CPUs per Task:")
            yield Input(placeholder="1", id="cpus_per_task", value="1")

            # Memory
            yield Static("Memory per Node (MB):")
            yield Input(placeholder="1024", id="mem_per_cpu", value="1024")

            # Time limit
            yield Static("Time Limit (hours:minutes:seconds):")
            yield Input(placeholder="01:00:00", id="time_limit", value="01:00:00")

            # Working directory
            yield Static("Working Directory:")
            yield Input(
                placeholder=f"{os.getcwd()}", id="working_dir", value=f"{os.getcwd()}"
            )

            # Job script
            yield Static("Job Command/Script:")
            yield Input(
                placeholder="Command or script to run", id="job_command", value=""
            )

            # Output file
            yield Static("Standard Output File:")
            yield Input(
                placeholder="slurm-%j.out", id="output_file", value="slurm-%j.out"
            )

            # Error file
            yield Static("Standard Error File:")
            yield Input(
                placeholder="slurm-%j.err", id="error_file", value="slurm-%j.err"
            )

            hz = Horizontal()
            hz.styles.align = ("center", "middle")

            with hz:
                submit_button = Button("Submit Job", variant="success", id="submit_job")
                submit_button.styles.width = 20
                submit_button.styles.height = 10
                submit_button.styles.padding = (1, 2)
                submit_button.styles.content_align = ("center", "middle")
                submit_button.styles.margin = (0, 1)

                clear_button = Button("Clear Form", id="clear_form")
                clear_button.styles.width = 20
                clear_button.styles.height = 10
                clear_button.styles.padding = (1, 2)
                clear_button.styles.content_align = ("center", "middle")
                clear_button.styles.margin = (0, 1)

                yield submit_button
                yield clear_button
            yield self.submit_status

    def on_mount(self) -> None:
        """Set up the widget when mounted"""
        self.load_partitions()
        self.status_message.update(
            "Configure your job parameters and click Submit Job when ready."
        )
        scroll_view = self.query_one("#form_scroll", expect_type=VerticalScroll)
        scroll_view.styles.height = "100%"
        scroll_view.styles.overflow_y = "scroll"
        scroll_view.can_focus = True

    def load_partitions(self) -> None:
        """Load available partitions into the dropdown"""
        if not SlurmInfo.is_slurm_available():
            return

        try:
            # Get partition information
            cmd = ["sinfo", "--format=%P", "--noheader"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            partitions = []
            for line in result.stdout.strip().split("\n"):
                if line:
                    partitions.append(
                        (
                            remove_suffix(line.strip(), "*"),
                            remove_suffix(line.strip(), "*"),
                        )
                    )

            self.partitions = partitions

            # Update the select widget
            partition_select = self.query_one("#partition", expect_type=Select)

            if partitions:
                options = []
                for value, label in partitions:
                    options.append(tuple([label, value]))
                partition_select.set_options(options)
                partition_select.value = partitions[0][0]
                self.status_message.update(
                    f"Loaded {len(partitions)} partitions successfully"
                )
            else:
                self.status_message.update("No partitions found in Slurm configuration")

        except Exception as e:
            self.status_message.update(f"[red]Error loading partitions: {e}[/red]")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        button_id = event.button.id

        if button_id == "submit_job":
            self.submit_job()
        elif button_id == "clear_form":
            self.clear_form()

    def submit_job(self) -> None:
        """Collect form data and submit the job"""
        try:
            # Get form values
            job_name = (
                self.query_one("#job_name", expect_type=Input).value or "slurm_job"
            )
            partition = self.query_one("#partition", expect_type=Select).value
            nodes = self.query_one("#nodes", expect_type=Input).value or "1"
            cpus_per_task = (
                self.query_one("#cpus_per_task", expect_type=Input).value or "1"
            )
            mem_per_cpu = (
                self.query_one("#mem_per_cpu", expect_type=Input).value or "1024"
            )
            time_limit = (
                self.query_one("#time_limit", expect_type=Input).value or "01:00:00"
            )
            working_dir = (
                self.query_one("#working_dir", expect_type=Input).value or os.getcwd()
            )
            job_command = self.query_one("#job_command", expect_type=Input).value
            output_file = (
                self.query_one("#output_file", expect_type=Input).value
                or "slurm-%j.out"
            )
            error_file = (
                self.query_one("#error_file", expect_type=Input).value or "slurm-%j.err"
            )

            # Validate required fields
            if not job_command:
                self.submit_status.update("[red]Error: Job command is required[/red]")
                return

            # Create a temporary job script
            temp_script = self._create_job_script(
                job_name,
                partition,
                nodes,
                cpus_per_task,
                mem_per_cpu,
                time_limit,
                working_dir,
                job_command,
                output_file,
                error_file,
            )

            # Submit the job
            cmd = ["sbatch", temp_script]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            # Parse the output to get the job ID
            job_id = result.stdout.strip().split()[-1]

            self.submit_status.update(
                f"[green]Job submitted successfully! Job ID: {job_id}[/green]"
            )

            # Clean up the temporary script file
            try:
                os.remove(temp_script)
            except:
                pass

        except subprocess.CalledProcessError as e:
            self.submit_status.update(f"[red]Error submitting job: {e.stderr}[/red]")
        except Exception as e:
            self.submit_status.update(f"[red]Error: {str(e)}[/red]")

    def _create_job_script(
        self,
        job_name,
        partition,
        nodes,
        cpus_per_task,
        mem_per_cpu,
        time_limit,
        working_dir,
        job_command,
        output_file,
        error_file,
    ):
        """Create a temporary job script file"""
        import tempfile

        # Create a temporary file
        fd, path = tempfile.mkstemp(suffix=".sh")

        try:
            with os.fdopen(fd, "w") as f:
                f.write("#!/bin/bash\n\n")
                f.write(f"#SBATCH --job-name={job_name}\n")
                f.write(f"#SBATCH --partition={partition}\n")
                f.write(f"#SBATCH --nodes={nodes}\n")
                f.write(f"#SBATCH --cpus-per-task={cpus_per_task}\n")
                f.write(f"#SBATCH --mem {mem_per_cpu}M\n")
                f.write(f"#SBATCH --time={time_limit}\n")
                f.write(f"#SBATCH --chdir={working_dir}\n")
                f.write(f"#SBATCH --output={output_file}\n")
                f.write(f"#SBATCH --error={error_file}\n")
                f.write("\n")
                f.write(f"cd {working_dir}\n\n")
                f.write(f"{job_command}\n")
        except Exception as e:
            os.remove(path)
            raise e

        return path

    def clear_form(self) -> None:
        """Reset all form fields to default values"""
        self.query_one("#job_name", expect_type=Input).value = ""
        partition_select = self.query_one("#partition", expect_type=Select)
        if self.partitions:
            partition_select.value = self.partitions[0][0]
        self.query_one("#nodes", expect_type=Input).value = "1"
        self.query_one("#cpus_per_task", expect_type=Input).value = "1"
        self.query_one("#mem_per_cpu", expect_type=Input).value = "1024"
        self.query_one("#time_limit", expect_type=Input).value = "01:00:00"
        self.query_one("#working_dir", expect_type=Input).value = os.getcwd()
        self.query_one("#job_command", expect_type=Input).value = ""
        self.query_one("#output_file", expect_type=Input).value = "slurm-%j.out"
        self.query_one("#error_file", expect_type=Input).value = "slurm-%j.err"
        self.submit_status.update("")


class JobMonitorView(Container):
    """View to monitor job output logs in real-time"""

    current_job_id = None
    refresh_timer: Optional[Timer] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_message = Static("")
        self.stdout_content = Static("")
        self.stderr_content = Static("")
        self.stdout_path = None
        self.stderr_path = None
        self.last_stdout_pos = 0
        self.last_stderr_pos = 0

    def compose(self) -> ComposeResult:
        """Compose the job monitor view with output and error logs"""
        yield self.status_message

        with Horizontal():
            # STDOUT section
            stdout_container = VerticalScroll()
            stdout_container.border_title = "Standard Output (stdout)"
            stdout_container.styles.border = ("heavy", "white")
            stdout_container.styles.width = "50%"
            stdout_container.styles.height = "100%"

            with stdout_container:
                yield self.stdout_content

            # STDERR section
            stderr_container = VerticalScroll()
            stderr_container.border_title = "Standard Error (stderr)"
            stderr_container.styles.border = ("heavy", "red")
            stderr_container.styles.width = "50%"
            stderr_container.styles.height = "100%"

            with stderr_container:
                yield self.stderr_content

    def start_monitoring(self, job_id: str) -> None:
        """Start monitoring the specified job"""
        self.current_job_id = job_id
        self.stdout_path = None
        self.stderr_path = None
        self.last_stdout_pos = 0
        self.last_stderr_pos = 0

        # Find the log files for this job
        job_details = SlurmInfo.get_job_details(job_id)

        if not job_details:
            self.status_message.update(
                f"[red]Error: Could not retrieve details for job {job_id}[/red]"
            )
            return

        # Extract stdout and stderr paths
        working_dir = job_details.get("WorkDir", os.getcwd())
        stdout_file = job_details.get("StdOut", f"slurm-{job_id}.out")
        stderr_file = job_details.get("StdErr", f"slurm-{job_id}.err")

        # Check if path is absolute, if not, prepend working directory
        if not os.path.isabs(stdout_file):
            stdout_file = os.path.join(working_dir, stdout_file)
        if not os.path.isabs(stderr_file):
            stderr_file = os.path.join(working_dir, stderr_file)

        # Replace %j with the job ID if present
        stdout_file = stdout_file.replace("%j", job_id)
        stderr_file = stderr_file.replace("%j", job_id)

        self.stdout_path = stdout_file
        self.stderr_path = stderr_file

        # Update status
        self.status_message.update(
            f"Monitoring job {job_id}\nStdOut: {stdout_file}\nStdErr: {stderr_file}"
        )

        # Start refreshing
        self.refresh_logs()

    def refresh_logs(self) -> None:
        """Refresh the log content from files"""
        if not self.current_job_id:
            return

        # Refresh stdout
        if self.stdout_path:
            self._refresh_stdout()

        # Refresh stderr
        if self.stderr_path:
            self._refresh_stderr()

        # Check if job is still running
        job_details = SlurmInfo.get_job_details(self.current_job_id)
        job_state = job_details.get("JobState", "UNKNOWN")

        if job_state in ["COMPLETED", "FAILED", "CANCELLED", "TIMEOUT"]:
            self.status_message.update(
                f"Job {self.current_job_id} has ended with state: {job_state}"
            )
        else:
            self.status_message.update(
                f"Monitoring job {self.current_job_id} (State: {job_state})"
            )

        # Set up the next refresh
        if self.refresh_timer:
            self.refresh_timer.stop()

        self.refresh_timer = self.set_interval(2, self.refresh_logs, repeat=1)

    def _refresh_stdout(self) -> None:
        """Refresh the stdout content from file"""
        try:
            if not os.path.exists(self.stdout_path):
                self.stdout_content.update(
                    f"[yellow]File not found: {self.stdout_path}[/yellow]"
                )
                return

            with open(self.stdout_path, "r") as f:
                # Seek to the last position we read
                f.seek(self.last_stdout_pos)

                # Read new content
                new_content = f.read()

                # Update the last position
                self.last_stdout_pos = f.tell()

            if new_content:
                # Append new content to the display
                current_content = self.stdout_content.renderable
                if current_content:
                    self.stdout_content.update(str(current_content) + new_content)
                else:
                    self.stdout_content.update(new_content)
        except Exception as e:
            self.stdout_content.update(f"[red]Error reading stdout: {str(e)}[/red]")

    def _refresh_stderr(self) -> None:
        """Refresh the stderr content from file"""
        try:
            if not os.path.exists(self.stderr_path):
                self.stderr_content.update(
                    f"[yellow]File not found: {self.stderr_path}[/yellow]"
                )
                return

            with open(self.stderr_path, "r") as f:
                # Seek to the last position we read
                f.seek(self.last_stderr_pos)

                # Read new content
                new_content = f.read()

                # Update the last position
                self.last_stderr_pos = f.tell()

            if new_content:
                # Append new content to the display
                current_content = self.stderr_content.renderable
                if current_content:
                    self.stderr_content.update(str(current_content) + new_content)
                else:
                    self.stderr_content.update(new_content)
        except Exception as e:
            self.stderr_content.update(f"[red]Error reading stderr: {str(e)}[/red]")

    def stop_monitoring(self) -> None:
        """Stop monitoring the current job"""
        self.current_job_id = None

        if self.refresh_timer:
            self.refresh_timer.stop()
            self.refresh_timer = None

        self.status_message.update("Job monitoring stopped.")


class SlurmPilotApp(App):
    """Slurm Job Monitor Application with multiple views"""

    TITLE = "Slurm Pilot"
    CSS_PATH = "style.css"  # We'll create this CSS file

    BINDINGS = [Binding("q", "quit", description="Quit")]

    # Define view IDs for navigation
    VIEW_JOBS = "jobs"
    VIEW_HARDWARE = "hardware"
    VIEW_SUBMITTER = "submitter"
    VIEW_MONITOR = "monitor"

    # Current active view
    current_view = VIEW_JOBS

    # Job being monitored
    monitored_job_id = None

    def compose(self) -> ComposeResult:
        """Create child widgets for the app"""
        yield Header()

        if SlurmInfo.is_slurm_available():
            # Create all views but only show the jobs view initially
            yield SlurmJobsView(id=self.VIEW_JOBS)
            yield HardwareConfigView(id=self.VIEW_HARDWARE, classes="hidden")
            yield JobSubmitterView(id=self.VIEW_SUBMITTER, classes="hidden")
            yield JobMonitorView(id=self.VIEW_MONITOR, classes="hidden")
        else:
            yield SlurmNotAvailableBanner()

        yield Footer()

    def on_mount(self) -> None:
        """Handle app initialization when mounted"""
        if SlurmInfo.is_slurm_available():
            # Update the bindings based on the current view
            self._update_bindings()

    def _update_bindings(self) -> None:
        """Update the key bindings based on the current view"""
        updating_keys = ["r", "h", "j", "m", "b", "c"]
        existing = dict(self._bindings)
        for key in list(existing.keys()):
            if key in updating_keys:
                existing.pop(key)
        existing = {key: [value] for key, value in existing.items()}
        self._bindings = BindingsMap.from_keys(existing)
        self.bind("q", "quit", description="Quit")

        if self.current_view == self.VIEW_JOBS:
            self.bind("r", "refresh", description="Refresh")
            self.bind("h", "show_hardware", description="Hardware")
            self.bind("j", "show_submitter", description="Submit New Job")
            self.bind("m", "monitor_job", description="Monitor Current Job")
            self.bind("c", "cancel_job", description="Cancel Current Job")
        elif self.current_view == self.VIEW_HARDWARE:
            self.bind("r", "refresh", description="Refresh")
            self.bind("b", "go_back", description="Back to Jobs")
        elif self.current_view == self.VIEW_SUBMITTER:
            self.bind("b", "go_back", description="Back to Jobs")
        elif self.current_view == self.VIEW_MONITOR:
            self.bind("r", "refresh", description="Refresh")
            self.bind("b", "go_back", description="Back to Jobs")
        self.refresh_bindings()

    # In the SlurmMonitorApp class, modify the _show_view method:
    def _show_view(self, view_id: str) -> None:
        """Switch to the specified view"""
        # Hide all views
        for view_name in [
            self.VIEW_JOBS,
            self.VIEW_HARDWARE,
            self.VIEW_SUBMITTER,
            self.VIEW_MONITOR,
        ]:
            try:
                view = self.query_one(f"#{view_name}")
                if view_name == view_id:
                    view.remove_class("hidden")
                    # Refresh data when showing a view
                    if view_name == self.VIEW_SUBMITTER:
                        submitter_view = self.query_one(
                            f"#{self.VIEW_SUBMITTER}", expect_type=JobSubmitterView
                        )
                        submitter_view.load_partitions()
                else:
                    view.add_class("hidden")
            except Exception:
                pass

        # Update current view
        self.current_view = view_id

        # Update the key bindings
        self._update_bindings()

        # Update title
        if view_id == self.VIEW_JOBS:
            self.title = "Slurm Job Monitor - Jobs"
        elif view_id == self.VIEW_HARDWARE:
            self.title = "Slurm Job Monitor - Hardware Configuration"
        elif view_id == self.VIEW_SUBMITTER:
            self.title = "Slurm Job Monitor - Job Submitter"
        elif view_id == self.VIEW_MONITOR:
            self.title = "Slurm Job Monitor - Job Output"

    def action_refresh(self) -> None:
        """Refresh the current view"""
        if self.current_view == self.VIEW_JOBS:
            jobs_view = self.query_one(f"#{self.VIEW_JOBS}", expect_type=SlurmJobsView)
            jobs_view.refresh_jobs()
        elif self.current_view == self.VIEW_HARDWARE:
            hardware_view = self.query_one(
                f"#{self.VIEW_HARDWARE}", expect_type=HardwareConfigView
            )
            hardware_view.refresh_hardware_info()

    def action_show_hardware(self) -> None:
        """Switch to the hardware configuration view"""
        self._show_view(self.VIEW_HARDWARE)

    def action_show_submitter(self) -> None:
        """Switch to the job submitter view"""
        self._show_view(self.VIEW_SUBMITTER)

    def action_go_back(self) -> None:
        """Go back to the jobs view"""
        # Stop monitoring if active
        if self.current_view == self.VIEW_MONITOR:
            monitor_view = self.query_one(
                f"#{self.VIEW_MONITOR}", expect_type=JobMonitorView
            )
            monitor_view.stop_monitoring()

        self._show_view(self.VIEW_JOBS)

    def action_monitor_job(self) -> None:
        """Start monitoring the selected job"""
        if self.current_view == self.VIEW_JOBS:
            jobs_view = self.query_one(f"#{self.VIEW_JOBS}", expect_type=SlurmJobsView)

            # Get the selected job ID
            if jobs_view.jobs and jobs_view.table.cursor_row >= 0:
                job_id = str(jobs_view.jobs[jobs_view.table.cursor_row]["id"])

                # Switch to the monitor view
                self._show_view(self.VIEW_MONITOR)

                # Start monitoring the job
                monitor_view = self.query_one(
                    f"#{self.VIEW_MONITOR}", expect_type=JobMonitorView
                )
                monitor_view.start_monitoring(job_id)

    def action_cancel_job(self) -> None:
        """Cancel the selected job"""
        if self.current_view == self.VIEW_JOBS:
            jobs_view = self.query_one(f"#{self.VIEW_JOBS}", expect_type=SlurmJobsView)

            # Get the selected job ID
            if jobs_view.jobs and jobs_view.table.cursor_row >= 0:
                job_id = str(jobs_view.jobs[jobs_view.table.cursor_row]["id"])

                try:
                    # Run scancel command to cancel the job
                    cmd = ["scancel", job_id]
                    result = subprocess.run(
                        cmd, capture_output=True, text=True, check=True
                    )

                    # Provide feedback to the user
                    jobs_view.status_message.update(
                        f"Successfully cancelled job {job_id}"
                    )

                    # Refresh the job list to update the UI
                    jobs_view.refresh_jobs()
                except subprocess.CalledProcessError as e:
                    # Handle command execution error
                    jobs_view.status_message.update(
                        f"[red]Error cancelling job {job_id}: {e.stderr}[/red]"
                    )
                except Exception as e:
                    # Handle other unexpected errors
                    jobs_view.status_message.update(f"[red]Error: {str(e)}[/red]")
