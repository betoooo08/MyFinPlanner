export class Chart {
    constructor(context, config) {
      // Basic implementation to avoid errors
      this.context = context
      this.config = config
  
      console.log("Chart initialized with:", config)
    }
  
    update() {
      console.log("Chart updated")
    }
  
    destroy() {
      console.log("Chart destroyed")
    }
  }