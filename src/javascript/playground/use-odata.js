/**
 * OData sample.
 */
const e = React.createElement;

class ODataViewer extends React.Component {

  constructor(props) {
    super(props);
    this.state = { url: null, resource: null, error: false };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({url: event.target.value});
    if (this.state.url) {
      this.setState({['error']: false});
    } else {
      this.setState({['error']: true});
    }
  }

  handleSubmit(event) {
    event.preventDefault();
    if (!this.state.url) {
      this.setState({['error']: true});
      return;
    }
    this.fetchOData(this.state.url);
  }

  fetchOData(url) {
    fetch(url)
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        this.setState({resource: data});
      });
  }

  renderForm() {
    var cls = '';
    if (this.state.error) {
      cls = ' alert alert-danger';
    }
    return e("form", { className: "form", onSubmit: this.handleSubmit },
             e("div", { className: "row input-group" },
               e("input", {type: "text", placeholder: "OData v4 URL", className: "form-control col-sm-10" + cls, onChange: this.handleChange}),
               e("button", {className: "btn btn-primary col-sm-2", onClick: this.handleSubmit}, "Fetch")));
  }

  renderResource() {
    if (!this.state.resource) {
      return e("div", {}, "No resource");
    }
    let context = this.state.resource['@odata.context'];
    var contents = null;
    let keys = new Set();
    if (this.state.resource['@odata.id']) {
      Object.keys(this.state.resource).forEach((k) => { keys.add(k); });
      contents = e("div", {},
                   e("div", {className: "row"},
                     e("p", {className: "col-sm-2"}, "ID: "),
                     e("pre", {className: "col-sm-10"}, this.state.resource['@odata.id'])),
                   e("div", {className: "row"},
                     e("p", {className: "col-sm-2"}, "Keys: "),
                     e("p", {className: "col-sm-10"}, [...keys].join(", "))),
                   e("pre", {},
                     e("code", {}, JSON.stringify(this.state.resource, null, 2))));
    }
    else if (this.state.resource['value']) {
      this.state.resource['value'].forEach((v) => {
        Object.keys(v).forEach((k) => { keys.add(k); });
      });
      const headers = [...keys].map((k) => {
        return e("th", {}, k);
      });
      const rows = this.state.resource['value'].map((v, i) => {
        const cells = [...keys].map((k) => {
          return e("td", {}, JSON.stringify(v[k]));
        });
        return e("tr", {},
                 e("th", {}, i+1),
                 cells);
      });
      contents = e("table", {className: "table"},
                   e("thead", {},
                     e("tr", {}, e("th", {}, "#"), headers)),
                   e("tbody", {}, rows));
    }
    return e("div", {},
             e("h5", {}, "Context: " + context),
             e("div", {}, contents));
  }

  render() {
    return e("div", {},
             this.renderForm(),
             e("hr"),
             this.renderResource());
  }
}
