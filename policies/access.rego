# Application-level access control

package platform.demo

# Only authenticated users with role "risk_assessor" can invoke loan decision
default allow = false

allow {
    input.method == "POST"
    input.path == "/api/loan-decision"
    input.user.roles[_] == "risk_assessor"
}