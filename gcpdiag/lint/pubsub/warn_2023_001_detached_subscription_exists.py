# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Project should not have a detached subscription.

A detached subscription is one whose reading privilege from the topic
has been revoked; it's retained messages are also deleted.
To free up the quota, it should be deleted.
"""

from gcpdiag import lint, models
from gcpdiag.queries import pubsub


def run_rule(context: models.Context, report: lint.LintReportRuleInterface):
  """Check if the project has a detached subscription."""
  subscriptions = pubsub.get_subscription(context)
  if not subscriptions:
    report.add_skipped(None, "no subscriptions found")
  for _, subscription in sorted(subscriptions.items()):
    if subscription.is_detached():
      report.add_failed(subscription, "detached subscription found")
    else:
      report.add_ok(subscription)
