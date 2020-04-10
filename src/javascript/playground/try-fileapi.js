const e = React.createElement;

class FileList extends React.Component {

  constructor(props) {
    super(props);
    this.state = { files: null, dropZone: "inactive", contents: null, currentFile: null };
    this.handleDrop = this.handleDrop.bind(this);
    this.handleDragEnter = this.handleDragEnter.bind(this);
    this.handleDragOver = this.handleDragOver.bind(this);
    this.handleDragLeave = this.handleDragLeave.bind(this);
  }

  handleDrop(event) {
    event.preventDefault();
    this.setState({ dropZone: "inactive" });
    const files = event.dataTransfer.files;
    this.setState({ files: files });
    this.setState({ contents: null });
  }

  handleDragEnter(event) {
    event.preventDefault();
    this.setState({ dropZone: "active" });
  }

  handleDragOver(event) {
    event.preventDefault();
    event.dataTransfer.dropEffect = "copy";
  }

  handleDragLeave(event) {
    event.preventDefault();
    this.setState({ dropZone: "inactive" });
  }

  readFile(event) {
    const button = event.target;
    let index = button.getAttribute("data-index");
    const file = this.state.files[index];
    const reader = new FileReader();
    const self = this;
    this.setState({currentFile: file});
    // Set handlers for progress, success, and errors
    reader.onprogress = function(event) {};
    reader.onerror = function(event) {};
    reader.onload = function(event) {
      const fileString = event.target.result;
      self.setState({ ["contents"]: fileString });
    };
    reader.readAsText(file, "UTF-8");
  }

  renderDropZone() {
    var cls = "";
    if (this.state.dropZone === "active") {
      cls = " alert alert-danger";
    }
    return e("div",
             { className: cls, id: "dropZone",
               onDrop: this.handleDrop,
               onDragEnter: this.handleDragEnter,
               onDragOver: this.handleDragOver,
               onDragLeave: this.handleDragLeave },
             "Drop text files here");
  }

  renderFileInfo(index) {
    const file = this.state.files[index];
    var action = "See below";
    if (file !== this.state.currentFile) {
      action = e("button", {
                   className: "btn btn-primary",
                   onClick: (event) => this.readFile(event), "data-index": index },
                 "Read");
    }
    return e("tr", {},
            e("th", {}, index+1),
            e("td", {}, file.name),
            e("td", {}, file.type),
            e("td", {}, file.size),
            e("td", {}, file.lastModifiedDate ? file.lastModifiedDate.toLocaleDateString() : "n/a"),
            e("td", {}, action));
  }

  renderFiles() {
    const files = this.state.files;
    if (files === null) {
      return e("div", {}, "No files.");
    }
    const rows = [];
    for (var i = 0; i < this.state.files.length; i++) {
      rows.push(this.renderFileInfo(i));
    }
    return e("table", { className: "table" },
             e("thead", {},
               e("th", {}, "#"),
               e("th", {}, "File name"),
               e("th", {}, "File type"),
               e("th", {}, "Size"),
               e("th", {}, "Last modified at"),
               e("th", {}, "Action")),
             e("tbody", {}, rows));
  }

  renderFileContents() {
    const contents = this.state.contents;
    if (contents === null) {
      return e("div", {}, "No contents.");
    }
    return e("div", {},
             e("h5", {}, "Contents"),
             e("div", {className: "row"},
               e("code", {className: "col-sm-8"}, this.state.currentFile.name),
               e("span", {className: "col-sm-4"}, this.state.currentFile.type)),
             e("pre", {}, contents));
  }

  render() {
    return e("div", {},
             this.renderDropZone(),
             this.renderFiles(),
             this.renderFileContents());
  }
}
