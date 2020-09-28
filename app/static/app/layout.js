new Vue({
  delimiters: ["[[", "]]"],
  el: "#form",
  data: {
    showTeacherForm: false,
    showStudentForm: false,
    register: true,
  },
  methods: {
    teacherForm: function () {
      this.showTeacherForm = true;
      this.showStudentForm = false;
      this.register = false;
    },
    studentForm: function () {
      this.showStudentForm = true;
      this.register = false;
      this.showTeacherForm = false;
    },
  },
});
