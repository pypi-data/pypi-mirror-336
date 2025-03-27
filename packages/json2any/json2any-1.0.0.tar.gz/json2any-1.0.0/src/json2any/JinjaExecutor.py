from logging import getLogger
from pathlib import Path
from typing import Any, Dict, Optional

import jsonpath_ng as jpng
from jinja2 import Environment, BaseLoader

from json2any.Json2AnyException import Json2AnyException
from json2any.project.CopyDescriptor import CopyDescriptor
from json2any.project.Json2AnyDescriptor import Json2AnyDescriptor
from json2any.project.RenderDescriptor import RenderDescriptor

QUERY_DATA_KEY = 'query'


class JinjaExecutor:
    def __init__(self, template_loader: BaseLoader, runs_descriptor: Json2AnyDescriptor, data: Dict[str, Any],
                 out_dir: Optional[Path] = None):
        self.log = getLogger(self.__class__.__name__)
        self.environment = Environment(loader=template_loader)
        self.jobs_descriptor: Json2AnyDescriptor = runs_descriptor
        self.data = data
        self.out_dir = (out_dir or Path('.')).absolute()
        self.validate_jobs()

    def execute_runs(self):
        for job in self.jobs_descriptor.jobs:

            if not job.enabled:
                self.log.info(f'Run "{job.name}" disabled')
                continue

            out_dir = self.out_dir.absolute()
            if not out_dir.exists():
                out_dir.mkdir(parents=True)

            if isinstance(job, RenderDescriptor):
                self.execute_job_render(out_dir, job)

            elif isinstance(job, CopyDescriptor):
                self.execute_job_copy(out_dir, job)

            else:
                raise Json2AnyException(f'Unsupported job type: {job.__class__.__name__}')

        self.log.info("finished all jobs")

    def execute_job_copy(self, out_dir: Path, job_desc: CopyDescriptor):
        self.log.info(f'Executing Copy job: "{job_desc.name}"')
        pass

    def execute_job_render(self, out_dir: Path, job_desc: RenderDescriptor):
        self.log.info(f'Executing Render Job: "{job_desc.name}"')

        data = self.data.copy()

        if job_desc.query is None:
            query_data = None
        else:
            query_data = self.data_query(job_desc.query)
        if job_desc.query_for_each:
            if not isinstance(query_data, list):
                raise Json2AnyException(
                    f'In job: "{job_desc.name}" data query "{job_desc.query}" did not produce list despite "query_for_each" is set to true')

            for query_item in query_data:
                data[QUERY_DATA_KEY] = query_item
                self.render_file(out_dir, job_desc, data)
        else:
            data[QUERY_DATA_KEY] = query_data
            self.render_file(out_dir, job_desc, data)

    def render_file(self, out_dir: Path, render_desc: RenderDescriptor, data: Any):
        file_name_template = self.environment.from_string(render_desc.output_file_pattern)
        try:
            file_name = file_name_template.render(data)
        except Exception as e:
            raise Json2AnyException(
                f'Failed to render file name for run: "{render_desc.name}"; template: "{render_desc.output_file_pattern}"') from e
        out_file = out_dir / file_name

        if out_file.exists() and not render_desc.output_override:
            return

        out_file_dir = out_file.parent
        if not out_file_dir.exists():
            out_file_dir.mkdir(parents=True)
        template = self.environment.get_template(render_desc.template)

        with out_file.open('w') as f:
            for item in template.generate(data):
                f.write(item)

    def data_query(self, query: Optional[str]) -> Any:
        if query is None:
            return self.data

        matcher = jpng.parse(query)
        values = [m.value for m in matcher.find(self.data)]
        if len(values) == 0:
            self.log.warning('Data query "%s" returned empty list', query)

        return values[0]

    def validate_jobs(self):

        if len(self.jobs_descriptor.jobs) == 0:
            raise ValueError('No Jobs found in descriptor: %s', self.jobs_descriptor)

        pass
