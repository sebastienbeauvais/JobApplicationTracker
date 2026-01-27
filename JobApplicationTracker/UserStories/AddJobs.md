# Title
Add Jobs Applied To
## Description
As a user I want to be able to store details of jobs I have applied to. These details should include
- Job Title
- Company
- Estimate Compensation
- Application Date
- URL of job posting
- Resume used for application 
- Cover Letter used for application (optional)

## Acceptance Criteria
- Job Title should take a string input. This way numbers and characters are accepted
- Company should take a string input
- Estimated compensation should be stored as an integer
- Application date should be a date field. You should be able to insert dates from the past but will not be able to insert a date that is greater than the current date.
- URL of the job posting should be a string. We will need to refer to this URL later on to add a link to the page
- Resume used should be stored as a string (i.e. the filename of the resume used)
- Cover letter used should be stored as a string (i.e. the filename of the coverletter used)

## Logic

### Compensation
- User must specify compensation type: **Hourly** or **Annual**
- Supports a range with **minimum required**, **maximum optional**
- If only a single number is provided, use that as the minimum with no maximum
- Currency: Assume **USD**

### Resume & Cover Letter Fields
- Provide both **file upload** and **dropdown selection**
- Dropdown displays previously uploaded files so users don't need to re-upload the same resume/cover letter multiple times
- Resume is **required**, Cover Letter is **optional**

### Field Validation
| Field | Type | Limit | Required |
|-------|------|-------|----------|
| Job Title | String | 100 characters | Yes |
| Company | String | 50 characters | Yes |
| Compensation Min | Integer | - | Yes |
| Compensation Max | Integer | - | No |
| Compensation Type | Enum (Hourly/Annual) | - | Yes |
| Application Date | Date | Cannot be future date | Yes |
| URL | String | No limit, must be well-formatted URL | Yes |
| Resume | String (filename) | - | Yes |
| Cover Letter | String (filename) | - | No |

### Form Behavior
- Dedicated page at `/add-job` (not the homepage)
- After successful submission:
  1. Display success message indicating job was entered successfully
  2. Redirect to the jobs list page (`/jobs`)
- No cancel button required

### Frontend Theme
- Apple website inspired aesthetic (see Ui.md for full details)
- Clean, modern, minimal with generous whitespace
- Supports dark mode

### Default Values on Creation
- **Status**: Automatically set to "Applied"
- **Got Interview**: false
- **Coding Question Link**: null